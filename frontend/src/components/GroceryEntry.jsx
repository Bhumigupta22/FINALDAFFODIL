import React, { useState } from 'react';
import './GroceryEntry.css';

export function GroceryEntry({ onItemAdded, loading }) {
  const [formData, setFormData] = useState({
    item_name: '',
    category: 'produce',
    brand: '',
    size: '',
    price: '',
    description: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const categories = [
    'produce', 'dairy', 'meat', 'pantry', 'beverages', 
    'snacks', 'health', 'beauty', 'frozen', 'other'
  ];

  const brands = ['', 'organic', 'budget', 'premium', 'standard', 'natural'];
  const sizes = ['', 'small', 'medium', 'large', 'xl', 'mini', 'family', 'pack'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validation
    if (!formData.item_name.trim()) {
      setError('Item name is required');
      return;
    }

    if (!formData.price || parseFloat(formData.price) < 0) {
      setError('Valid price is required');
      return;
    }

    try {
      setIsLoading(true);
      
      const response = await fetch('http://localhost:5000/api/grocery/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          item_name: formData.item_name.trim(),
          category: formData.category,
          brand: formData.brand || null,
          size: formData.size || null,
          price: parseFloat(formData.price),
          description: formData.description || null
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to add item');
      }

      const data = await response.json();
      setSuccess(`✓ Added "${formData.item_name}" at $${formData.price}`);
      
      // Reset form
      setFormData({
        item_name: '',
        category: 'produce',
        brand: '',
        size: '',
        price: '',
        description: ''
      });

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);

      if (onItemAdded) {
        onItemAdded(data);
      }
    } catch (err) {
      setError(err.message || 'Failed to add grocery item');
      console.error('Error adding item:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="grocery-entry">
      <div className="entry-header">
        <h3>📦 Add Grocery Item with Price</h3>
        <p>Add items to the database for search and filtering</p>
      </div>

      {error && <div className="error-alert">{error}</div>}
      {success && <div className="success-alert">{success}</div>}

      <form onSubmit={handleSubmit} className="entry-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="item_name">Item Name *</label>
            <input
              id="item_name"
              type="text"
              name="item_name"
              placeholder="e.g., Organic Apples"
              value={formData.item_name}
              onChange={handleChange}
              disabled={isLoading || loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="price">Price ($) *</label>
            <input
              id="price"
              type="number"
              name="price"
              placeholder="e.g., 3.99"
              value={formData.price}
              onChange={handleChange}
              disabled={isLoading || loading}
              step="0.01"
              min="0"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              disabled={isLoading || loading}
            >
              {categories.map(cat => (
                <option key={cat} value={cat}>
                  {cat.charAt(0).toUpperCase() + cat.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="brand">Brand Type</label>
            <select
              id="brand"
              name="brand"
              value={formData.brand}
              onChange={handleChange}
              disabled={isLoading || loading}
            >
              {brands.map(brand => (
                <option key={brand} value={brand}>
                  {brand ? brand.charAt(0).toUpperCase() + brand.slice(1) : 'None'}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="size">Size</label>
            <select
              id="size"
              name="size"
              value={formData.size}
              onChange={handleChange}
              disabled={isLoading || loading}
            >
              {sizes.map(size => (
                <option key={size} value={size}>
                  {size ? size.charAt(0).toUpperCase() + size.slice(1) : 'None'}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group full-width">
            <label htmlFor="description">Description</label>
            <input
              id="description"
              type="text"
              name="description"
              placeholder="e.g., Fresh organic granny smith apples"
              value={formData.description}
              onChange={handleChange}
              disabled={isLoading || loading}
            />
          </div>
        </div>

        <button
          type="submit"
          className="submit-button"
          disabled={isLoading || loading}
        >
          {isLoading ? 'Adding...' : '➕ Add Item'}
        </button>
      </form>
    </div>
  );
}
