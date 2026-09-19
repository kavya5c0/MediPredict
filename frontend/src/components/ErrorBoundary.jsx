import { Component } from 'react'
import { AlertCircle, RefreshCw, Home } from 'lucide-react'
import { Link } from 'react-router-dom'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    })
    
    // Log error to console
    console.error('ErrorBoundary caught an error:', error, errorInfo)
    
    // You could also log to an error reporting service here
    // logErrorToService(error, errorInfo)
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center px-4">
          <div className="max-w-lg w-full">
            <div className="bg-white rounded-2xl shadow-2xl p-8">
              <div className="flex flex-col items-center text-center">
                <div className="p-4 bg-red-100 rounded-full mb-6">
                  <AlertCircle className="h-12 w-12 text-red-600" />
                </div>
                
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  Oops! Something went wrong
                </h1>
                
                <p className="text-gray-600 mb-6">
                  We encountered an unexpected error. Don't worry, your data is safe.
                </p>

                {this.state.error && (
                  <div className="bg-gray-50 rounded-lg p-4 mb-6 text-left w-full">
                    <p className="text-sm font-medium text-gray-700 mb-2">Error details:</p>
                    <p className="text-xs text-gray-600 font-mono break-all">
                      {this.state.error.toString()}
                    </p>
                  </div>
                )}

                <div className="flex flex-col sm:flex-row gap-3 w-full">
                  <button
                    onClick={this.handleReset}
                    className="flex-1 flex items-center justify-center space-x-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
                  >
                    <RefreshCw className="h-4 w-4" />
                    <span>Try Again</span>
                  </button>
                  
                  <Link
                    to="/"
                    className="flex-1 flex items-center justify-center space-x-2 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    <Home className="h-4 w-4" />
                    <span>Go Home</span>
                  </Link>
                </div>

                <p className="text-xs text-gray-500 mt-6">
                  If this problem persists, please contact support or try refreshing the page.
                </p>
              </div>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary