import React, { useState } from 'react';
import { searchAPI } from '../api';
import './PriceFilter.css';

export function PriceFilter({ onResults, loading }) {
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [brand, setBrand] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const brands = ['', 'organic', 'budget', 'premium'];

  const handleFilter = async (e) => {
    e.preventDefault();
    
    if (!minPrice && !maxPrice) {
      alert('Please enter at least a minimum or maximum price');
      return;
    }

    try {
      setIsLoading(true);
      const filters = {
        min_price: minPrice ? parseFloat(minPrice) : null,
        max_price: maxPrice ? parseFloat(maxPrice) : null,
        brand: brand || null
      };

      const response = await searchAPI.filterByPrice(filters);
      onResults(response.data.results, `Price: $${minPrice || '0'} - $${maxPrice || 'Any'}`);
      setMinPrice('');
      setMaxPrice('');
      setBrand('');
    } catch (err) {
      console.error('Filter error:', err);
      alert('Failed to filter items');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="price-filter">
      <h4>💰 Filter by Price</h4>
      <form onSubmit={handleFilter} className="filter-form">
        <div className="filter-row">
          <div className="filter-group">
            <label htmlFor="minPrice">Min Price ($)</label>
            <input
              id="minPrice"
              type="number"
              placeholder="Min"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
              step="0.01"
              min="0"
              disabled={isLoading || loading}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="maxPrice">Max Price ($)</label>
            <input
              id="maxPrice"
              type="number"
              placeholder="Max"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              step="0.01"
              min="0"
              disabled={isLoading || loading}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="brand">Brand</label>
            <select
              id="brand"
              value={brand}
              onChange={(e) => setBrand(e.target.value)}
              disabled={isLoading || loading}
            >
              {brands.map((b) => (
                <option key={b} value={b}>
                  {b ? b.charAt(0).toUpperCase() + b.slice(1) : 'Any Brand'}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="filter-button"
            disabled={isLoading || loading || (!minPrice && !maxPrice)}
          >
            {isLoading ? 'Filtering...' : 'Filter'}
          </button>
        </div>
      </form>
    </div>
  );
}
