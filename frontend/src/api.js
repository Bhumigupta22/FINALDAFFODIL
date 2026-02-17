import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://finaldaffodil.onrender.com';

const api = axios.create({
  baseURL: `${API_URL}/api`
});

export const shoppingAPI = {
  getList: () => api.get('/shopping/list'),
  addItem: (item) => api.post('/shopping/add', item),
  removeItem: (itemId) => api.delete(`/shopping/${itemId}`),
  completeItem: (itemId) => api.put(`/shopping/${itemId}/complete`),
  updateItem: (itemId, data) => api.put(`/shopping/${itemId}`, data)
};

export const voiceAPI = {
  processCommand: (text) => api.post('/voice/process', { text }),
  transcribeAudio: (audioFile, language = 'en-US') => {
    const formData = new FormData();
    formData.append('audio', audioFile);
    formData.append('language', language);
    return api.post('/voice/transcribe', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  getLanguages: () => api.get('/voice/languages')
};

export const suggestionsAPI = {
  getSmartSuggestions: () => api.get('/suggestions/'),
  getHistory: () => api.get('/suggestions/history')
};
export const searchAPI = {
  searchItems: (query) => api.post('/search/items', { text: query }),
  filterByPrice: (filters) => api.post('/search/by-price', filters),
  voiceSearch: (text) => api.post('/search/voice', { text })
};
