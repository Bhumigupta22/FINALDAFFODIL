import React, { useState, useEffect, useCallback } from 'react';
import { VoiceInput } from './components/VoiceInput';
import { ShoppingList } from './components/ShoppingList';
import { Suggestions } from './components/Suggestions';
import { PriceFilter } from './components/PriceFilter';
import { GroceryEntry } from './components/GroceryEntry';
import SearchResults from './components/SearchResults';
import { shoppingAPI, voiceAPI } from './api';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastCommand, setLastCommand] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  const handleFilterResults = (results, query) => {
    setSearchResults(results);
    setSearchQuery(query);
  };

  useEffect(() => {
    loadShoppingList();
  }, []);

  const loadShoppingList = async () => {
    try {
      setLoading(true);
      const response = await shoppingAPI.getList();
      setItems(response.data.items || []);
      setError(null);
    } catch (err) {
      setError('Failed to load shopping list');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceText = async (text) => {
    try {
      setLoading(true);
      setError(null);
      
      // Process the voice command
      const response = await voiceAPI.processCommand(text);
      setLastCommand(response.data);

      if (response.data.command === 'add') {
        // Add item to shopping list
        const addResponse = await shoppingAPI.addItem({
          item_name: response.data.item_name,
          category: response.data.category,
          quantity: response.data.quantity,
          unit: response.data.unit
        });
        
        const addedItem = addResponse.data.item;
        const existingIndex = items.findIndex(item => item.id === addedItem.id);
        if (existingIndex !== -1) {
          const updatedItems = [...items];
          updatedItems[existingIndex] = addedItem;
          setItems(updatedItems);
        } else {
          setItems([...items, addedItem]);
        }
        setSearchResults([]);
      } else if (response.data.command === 'remove') {
        // Handle remove command
        const itemToRemove = items.find(item =>
          item.item_name.toLowerCase().includes(response.data.item_name.toLowerCase())
        );
        
        if (itemToRemove) {
          await shoppingAPI.removeItem(itemToRemove.id);
          setItems(items.filter(item => item.id !== itemToRemove.id));
        }
        setSearchResults([]);
      } else if (response.data.command === 'search') {
        // Handle search command
        setSearchQuery(response.data.item_name);
        setSearchResults(response.data.search_results || []);
      } else if (response.data.command === 'filter') {
        // Handle filter command
        setSearchQuery('price filter');
        setSearchResults(response.data.filter_results || []);
      }
    } catch (err) {
      setError('Failed to process command');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async (itemData) => {
    try {
      setLoading(true);
      const response = await shoppingAPI.addItem(itemData);
      const addedItem = response.data.item;
      
      // Check if item already exists (update) or new (add)
      const existingIndex = items.findIndex(item => item.id === addedItem.id);
      if (existingIndex !== -1) {
        // Update existing item
        const updatedItems = [...items];
        updatedItems[existingIndex] = addedItem;
        setItems(updatedItems);
      } else {
        // Add new item
        setItems([...items, addedItem]);
      }
      setError(null);
    } catch (err) {
      setError('Failed to add item');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveItem = async (itemId) => {
    try {
      setLoading(true);
      await shoppingAPI.removeItem(itemId);
      setItems(items.filter(item => item.id !== itemId));
      setError(null);
    } catch (err) {
      setError('Failed to remove item');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteItem = async (itemId) => {
    try {
      setLoading(true);
      await shoppingAPI.completeItem(itemId);
      setItems(items.filter(item => item.id !== itemId));
      setError(null);
    } catch (err) {
      setError('Failed to complete item');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuantityChange = async (itemId, newQuantity) => {
    if (newQuantity < 1) {
      handleRemoveItem(itemId);
      return;
    }
    try {
      setLoading(true);
      const response = await shoppingAPI.updateItem(itemId, { quantity: newQuantity });
      const updatedItem = response.data.item;
      setItems(items.map(item => item.id === itemId ? updatedItem : item));
      setError(null);
    } catch (err) {
      setError('Failed to update quantity');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🛒 Voice Shopping Assistant</h1>
          <p>Speak to add items, search, filter by price, or get smart suggestions</p>
        </header>

        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        <VoiceInput onText={handleVoiceText} loading={loading} />

        {lastCommand && (
          <div className="last-command">
            <strong>Processing:</strong> {lastCommand.item_name}
            {lastCommand.quantity > 1 && ` (${lastCommand.quantity} ${lastCommand.unit})`}
          </div>
        )}

        <div className="content-grid">
          <div className="left-column">
            <GroceryEntry onItemAdded={() => {}} loading={loading} />
            
            <ShoppingList
              items={items}
              onItemRemove={handleRemoveItem}
              onItemComplete={handleCompleteItem}
              onQuantityChange={handleQuantityChange}
              loading={loading}
            />
          </div>

          <div className="right-column">
            <PriceFilter onResults={handleFilterResults} loading={loading} />
            
            {searchResults.length > 0 && (
              <SearchResults 
                results={searchResults} 
                onAddItem={handleAddItem}
                loading={loading}
                searchQuery={searchQuery}
              />
            )}
            
            <Suggestions items={items} onAddItem={handleAddItem} loading={loading} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
