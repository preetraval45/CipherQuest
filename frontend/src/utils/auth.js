// Authentication utility functions

/**
 * Store authentication token in localStorage
 * @param {string} token - JWT token
 */
export const storeAuthToken = (token) => {
  localStorage.setItem('authToken', token);
};

/**
 * Get authentication token from localStorage
 * @returns {string|null} JWT token or null if not found
 */
export const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

/**
 * Remove authentication token from localStorage
 */
export const removeAuthToken = () => {
  localStorage.removeItem('authToken');
};

/**
 * Check if user is authenticated
 * @returns {boolean} True if user has valid token
 */
export const isAuthenticated = () => {
  const token = getAuthToken();
  return token !== null && token !== 'undefined';
};

/**
 * Simulate authentication API call
 * @param {Object} credentials - User credentials
 * @param {boolean} isLogin - Whether this is a login or signup
 * @returns {Promise<Object>} Authentication response
 */
export const authenticateUser = async (credentials, isLogin = true) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Simulate successful authentication
  const mockToken = `mock-jwt-token-${Date.now()}`;
  
  return {
    access_token: mockToken,
    refresh_token: `mock-refresh-token-${Date.now()}`,
    user: {
      id: 1,
      username: credentials.email.split('@')[0],
      email: credentials.email,
      first_name: credentials.first_name || 'User',
      last_name: credentials.last_name || 'Name'
    }
  };
};

/**
 * Handle authentication error
 * @param {Error} error - Authentication error
 * @returns {string} User-friendly error message
 */
export const handleAuthError = (error) => {
  console.error('Authentication error:', error);
  return 'Authentication failed. Please try again.';
}; 