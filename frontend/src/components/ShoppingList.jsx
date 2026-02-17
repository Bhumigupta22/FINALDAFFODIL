import React, { useState, useEffect } from 'react';
import { shoppingAPI } from '../api';
import './ShoppingList.css';

export function ShoppingList({ items, onItemRemove, onItemComplete, onQuantityChange, loading }) {
  const [expandedCategory, setExpandedCategory] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Filter items by search query
  const filteredItems = items.filter(item =>
    item.item_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Group items by category
  const groupedItems = filteredItems.reduce((acc, item) => {
    const category = item.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(item);
    return acc;
  }, {});

  const getCategoryEmoji = (category) => {
    const emojis = {
      'dairy': '🥛',
      'produce': '🥬',
      'meat': '🥩',
      'snacks': '🍪',
      'beverages': '🥤',
      'pantry': '🍞',
      'other': '📦'
    };
    return emojis[category] || '📦';
  };

  return (
    <div className="shopping-list">
      <h2>Shopping List</h2>
      
      <div className="search-bar">
        <input
          type="text"
          placeholder="🔍 Search items..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        {searchQuery && (
          <button
            className="clear-search"
            onClick={() => setSearchQuery('')}
            title="Clear search"
          >
            ✕
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <p className="empty-state">No items yet. Add some using voice commands!</p>
      ) : filteredItems.length === 0 ? (
        <p className="empty-state">No items match "{searchQuery}". Try a different search.</p>
      ) : (
        <div className="categories">
          {Object.entries(groupedItems).map(([category, categoryItems]) => (
            <div key={category} className="category-group">
              <button
                className="category-header"
                onClick={() => setExpandedCategory(
                  expandedCategory === category ? null : category
                )}
              >
                <span className="category-emoji">{getCategoryEmoji(category)}</span>
                <span className="category-name">{category}</span>
                <span className="item-count">{categoryItems.length}</span>
                <span className="toggle">
                  {expandedCategory === category ? '▼' : '▶'}
                </span>
              </button>
              
              {expandedCategory === category && (
                <div className="items">
                  {categoryItems.map(item => (
                    <div key={item.id} className="item">
                      <div className="item-details">
                        <div className="item-name">{item.item_name}</div>
                        {item.quantity && (
                          <div className="item-quantity-control">
                            <button
                              className="qty-btn minus"
                              onClick={() => onQuantityChange(item.id, item.quantity - 1)}
                              disabled={loading}
                              title="Decrease quantity"
                            >
                              −
                            </button>
                            <span className="qty-display">
                              {item.quantity} {item.unit || 'qty'}
                            </span>
                            <button
                              className="qty-btn plus"
                              onClick={() => onQuantityChange(item.id, item.quantity + 1)}
                              disabled={loading}
                              title="Increase quantity"
                            >
                              +
                            </button>
                          </div>
                        )}
                      </div>
                      <div className="item-actions">
                        <button
                          className="action-btn complete"
                          onClick={() => onItemComplete(item.id)}
                          disabled={loading}
                          title="Mark as purchased"
                        >
                          ✓
                        </button>
                        <button
                          className="action-btn remove"
                          onClick={() => onItemRemove(item.id)}
                          disabled={loading}
                          title="Remove item"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
