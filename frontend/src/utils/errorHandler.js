/**
 * Error Handler Utilities
 * Provides user-friendly error messages and error handling functions
 */

// Error message mapping for common errors
const ERROR_MESSAGES = {
  // Network errors
  NETWORK_ERROR: 'Unable to connect to the server. Please check your internet connection.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.',
  
  // Authentication errors
  UNAUTHORIZED: 'Please log in to access this feature.',
  INVALID_CREDENTIALS: 'Invalid email or password. Please try again.',
  TOKEN_EXPIRED: 'Your session has expired. Please log in again.',
  ACCOUNT_LOCKED: 'Your account has been locked. Please contact support.',
  
  // Validation errors
  INVALID_EMAIL: 'Please enter a valid email address.',
  INVALID_PASSWORD: 'Password must be at least 8 characters long.',
  PASSWORD_MISMATCH: 'Passwords do not match.',
  REQUIRED_FIELD: 'This field is required.',
  INVALID_FORMAT: 'Invalid format. Please check your input.',
  
  // API errors
  SERVER_ERROR: 'Something went wrong on our end. Please try again later.',
  NOT_FOUND: 'The requested resource was not found.',
  CONFLICT: 'This information already exists.',
  FORBIDDEN: 'You do not have permission to perform this action.',
  
  // File upload errors
  FILE_TOO_LARGE: 'File is too large. Maximum size is 10MB.',
  INVALID_FILE_TYPE: 'Invalid file type. Please upload an image or PDF.',
  UPLOAD_FAILED: 'Failed to upload file. Please try again.',
  
  // Medical specific errors
  ANALYSIS_FAILED: 'Failed to analyze medical report. Please try again.',
  PREDICTION_FAILED: 'Failed to generate prediction. Please ensure all fields are filled.',
  CHAT_FAILED: 'Failed to send message. Please try again.',
  
  // Generic errors
  UNKNOWN_ERROR: 'An unexpected error occurred. Please try again.',
};

/**
 * Get user-friendly error message
 * @param {Error} error - The error object
 * @returns {string} User-friendly error message
 */
export const getErrorMessage = (error) => {
  if (!error) return ERROR_MESSAGES.UNKNOWN_ERROR;

  // Handle axios errors
  if (error.response) {
    const status = error.response.status;
    const data = error.response.data;

    switch (status) {
      case 400:
        return data?.detail || data?.message || ERROR_MESSAGES.INVALID_FORMAT;
      case 401:
        return ERROR_MESSAGES.UNAUTHORIZED;
      case 403:
        return ERROR_MESSAGES.FORBIDDEN;
      case 404:
        return ERROR_MESSAGES.NOT_FOUND;
      case 409:
        return ERROR_MESSAGES.CONFLICT;
      case 422:
        return data?.detail || ERROR_MESSAGES.INVALID_FORMAT;
      case 429:
        return 'Too many requests. Please wait a moment and try again.';
      case 500:
        return ERROR_MESSAGES.SERVER_ERROR;
      case 502:
      case 503:
      case 504:
        return 'Service temporarily unavailable. Please try again later.';
      default:
        return data?.detail || data?.message || ERROR_MESSAGES.UNKNOWN_ERROR;
    }
  }

  // Handle network errors
  if (error.message) {
    if (error.message.includes('Network Error')) {
      return ERROR_MESSAGES.NETWORK_ERROR;
    }
    if (error.message.includes('timeout')) {
      return ERROR_MESSAGES.TIMEOUT_ERROR;
    }
    if (error.message.includes('401')) {
      return ERROR_MESSAGES.UNAUTHORIZED;
    }
  }

  // Handle specific error codes
  if (error.code === 'ECONNABORTED') {
    return ERROR_MESSAGES.TIMEOUT_ERROR;
  }

  return ERROR_MESSAGES.UNKNOWN_ERROR;
};

/**
 * Handle API error with user-friendly message
 * @param {Error} error - The error object
 * @param {Function} setError - Function to set error state
 * @param {Object} options - Additional options
 */
export const handleApiError = (error, setError, options = {}) => {
  const { showMessage = true, logError = true } = options;
  
  const message = getErrorMessage(error);
  
  if (logError) {
    console.error('API Error:', error);
  }
  
  if (showMessage && setError) {
    setError(message);
  }
  
  return message;
};

/**
 * Check if error is authentication related
 * @param {Error} error - The error object
 * @returns {boolean}
 */
export const isAuthError = (error) => {
  if (error.response?.status === 401) return true;
  if (error.message?.includes('401')) return true;
  if (error.message?.includes('Unauthorized')) return true;
  return false;
};

/**
 * Check if error is network related
 * @param {Error} error - The error object
 * @returns {boolean}
 */
export const isNetworkError = (error) => {
  if (error.message?.includes('Network Error')) return true;
  if (error.code === 'ECONNABORTED') return true;
  if (!error.response && error.message) return true;
  return false;
};

/**
 * Check if error is validation error
 * @param {Error} error - The error object
 * @returns {boolean}
 */
export const isValidationError = (error) => {
  if (error.response?.status === 422) return true;
  if (error.response?.status === 400) return true;
  return false;
};

/**
 * Get validation errors from response
 * @param {Error} error - The error object
 * @returns {Object} Validation errors
 */
export const getValidationErrors = (error) => {
  if (!error.response?.data) return {};
  
  const data = error.response.data;
  
  // Handle different error response formats
  if (data.detail) {
    if (typeof data.detail === 'string') {
      return { general: data.detail };
    }
    if (Array.isArray(data.detail)) {
      return data.detail.reduce((acc, err) => {
        const field = err.loc?.[1] || 'general';
        acc[field] = err.msg;
        return acc;
      }, {});
    }
  }
  
  if (data.errors) {
    return data.errors;
  }
  
  return {};
};

export default ERROR_MESSAGES;