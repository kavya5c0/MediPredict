import { Toaster } from 'react-hot-toast'
import { useEffect } from 'react'

const ToastProvider = () => {
  useEffect(() => {
    // Configure toast defaults
    const style = {
      background: '#363636',
      color: '#fff',
      padding: '16px',
      borderRadius: '8px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    }

    const successStyle = {
      ...style,
      background: '#22c55e',
    }

    const errorStyle = {
      ...style,
      background: '#ef4444',
    }

    const infoStyle = {
      ...style,
      background: '#3b82f6',
    }

    // Add custom styles (this would need additional configuration)
  }, [])

  return (
    <Toaster
      position="top-right"
      reverseOrder={false}
      gutter={8}
      containerStyle={{}}
      toastOptions={{
        duration: 4000,
        style: {
          background: '#363636',
          color: '#fff',
        },
        success: {
          duration: 3000,
          iconTheme: {
            primary: '#22c55e',
            secondary: '#fff',
          },
        },
        error: {
          duration: 5000,
          iconTheme: {
            primary: '#ef4444',
            secondary: '#fff',
          },
        },
        loading: {
          duration: Infinity,
        },
      }}
    />
  )
}

export default ToastProvider