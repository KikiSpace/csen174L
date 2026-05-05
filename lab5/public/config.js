/**
 * API Configuration
 *
 * This file manages the API endpoint URL for different environments:
 * - Development: Uses local server (http://localhost:3000)
 * - Production (GitHub Pages): Uses deployed backend URL
 */

const CONFIG = {
  // Default to local development server
  API_URL: 'http://localhost:3000',

  // Override for production (GitHub Pages)
  // Set this to your deployed backend URL (Render, Railway, Vercel, etc.)
  PRODUCTION_API_URL: 'https://csen174l.onrender.com', // Change this!

  // Auto-detect environment
  getApiUrl() {
    // If we're on GitHub Pages (or any non-localhost domain), use production URL
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      return this.PRODUCTION_API_URL;
    }
    return this.API_URL;
  }
};

// Export for use in app.js
const API_BASE_URL = CONFIG.getApiUrl();

console.log('🌐 API Configuration:', {
  hostname: window.location.hostname,
  apiUrl: API_BASE_URL,
  environment: API_BASE_URL.includes('localhost') ? 'development' : 'production'
});
