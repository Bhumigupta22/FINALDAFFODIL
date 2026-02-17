import React, { useState, useEffect } from 'react';
import '../styles/SearchResults.css';

const SearchResults = ({ results, onAddItem, loading = false, searchQuery = '' }) => {
  if (!results || results.length === 0) {
    return (
      <div className="search-results-empty">
        {loading ? (
          <p>Searching for items...</p>
        ) : searchQuery ? (
          <p>No items found for "{searchQuery}"</p>
        ) : (
          <p>Use voice search to find items</p>
        )}
      </div>
    );
  }

  const handleAddToCart = (item) => {
    onAddItem({
      item_name: item.item_name,
      category: item.category,
      quantity: 1,
      brand: item.brand,
      size: item.size,
      price: item.price
    });
  };

  return (
    <div className="search-results-container">
      <div className="search-results-header">
        <h3>Found {results.length} items</h3>
        {searchQuery && <p className="search-query">for: "{searchQuery}"</p>}
      </div>
      
      <div className="search-results-list">
        {results.map((item, index) => (
          <div key={index} className="search-result-item">
            <div className="result-info">
              <h4 className="result-name">{item.item_name}</h4>
              <div className="result-details">
                {item.category && <span className="badge category">{item.category}</span>}
                {item.brand && <span className="badge brand">{item.brand}</span>}
                {item.size && <span className="badge size">{item.size}</span>}
              </div>
              {item.description && <p className="result-description">{item.description}</p>}
            </div>
            
            <div className="result-price-action">
              {item.price && (
                <div className="result-price">
                  <span className="price-amount">${item.price.toFixed(2)}</span>
                </div>
              )}
              <button 
                className="btn-add-to-cart"
                onClick={() => handleAddToCart(item)}
                title="Add to shopping list"
              >
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
