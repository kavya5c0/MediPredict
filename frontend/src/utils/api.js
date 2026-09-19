import axios from 'axios'
import toast from 'react-hot-toast'
import { getErrorMessage, isAuthError, isNetworkError } from './errorHandler'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 second timeout
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// Handle errors
api.interceptors.response.use(
  response => response,
  async (error) => {
    const errorMessage = getErrorMessage(error)
    const shouldShowToast = error.config?.suppressErrorToast !== true
    
    // Handle authentication errors
    if (isAuthError(error)) {
      localStorage.removeItem('token')
      if (shouldShowToast) {
        toast.error('Your session has expired. Please log in again.')
      }
      setTimeout(() => {
        window.location.href = '/login'
      }, 1500)
      return Promise.reject(error)
    }
    
    // Handle network errors
    if (isNetworkError(error)) {
      if (shouldShowToast) {
        toast.error(errorMessage)
      }
      return Promise.reject(error)
    }
    
    // Show error toast for other errors (optional - can be disabled per request)
    if (shouldShowToast) {
      toast.error(errorMessage)
    }
    
    return Promise.reject(error)
  }
)

// Helper method to make requests without error toasts
const quietApi = {
  get: (url, config) => api.get(url, { ...config, suppressErrorToast: true }),
  post: (url, data, config) => api.post(url, data, { ...config, suppressErrorToast: true }),
  put: (url, data, config) => api.put(url, data, { ...config, suppressErrorToast: true }),
  delete: (url, config) => api.delete(url, { ...config, suppressErrorToast: true }),
  patch: (url, data, config) => api.patch(url, data, { ...config, suppressErrorToast: true }),
}

export default api
export { quietApi }
