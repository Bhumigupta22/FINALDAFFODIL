import React, { useState } from 'react';
import axios from 'axios';
import '../styles/DatasetUpload.css';

export function DatasetUpload({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.csv') && !file.name.endsWith('.json')) {
      setMessageType('error');
      setMessage('Please upload a CSV or JSON file');
      return;
    }

    try {
      setUploading(true);
      setMessage('');

      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        'http://localhost:5000/api/suggestions/apriori/upload',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      setMessageType('success');
      setMessage(response.data.message || `Dataset loaded! Found ${response.data.rules_count || 0} association rules.`);
      
      // Clear the input
      if (event.target) event.target.value = '';
      
      // Notify parent component
      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      setMessageType('error');
      setMessage(err.response?.data?.error || 'Failed to upload dataset');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="dataset-upload">
      <div className="upload-card">
        <h3>📊 Load Apriori Dataset</h3>
        <p>Upload a CSV or JSON file to train the Apriori algorithm</p>
        
        <label className="upload-label">
          <input
            type="file"
            accept=".csv,.json"
            onChange={handleFileUpload}
            disabled={uploading}
            className="file-input"
          />
          <span className="upload-button">
            {uploading ? 'Uploading...' : '📁 Choose File'}
          </span>
        </label>

        {message && (
          <div className={`upload-message ${messageType}`}>
            {messageType === 'success' ? '✅' : '❌'} {message}
          </div>
        )}
      </div>
    </div>
  );
}
