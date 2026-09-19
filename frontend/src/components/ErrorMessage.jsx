import { AlertCircle, X, Info, AlertTriangle, CheckCircle } from 'lucide-react'

const ErrorMessage = ({ 
  message, 
  type = 'error', 
  onDismiss, 
  showIcon = true,
  className = '' 
}) => {
  const icons = {
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
    success: CheckCircle
  }

  const styles = {
    error: 'bg-red-50 border-red-200 text-red-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
    success: 'bg-green-50 border-green-200 text-green-800'
  }

  const iconColors = {
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
    success: 'text-green-600'
  }

  const Icon = icons[type] || icons.error

  if (!message) return null

  return (
    <div className={`rounded-lg p-4 border flex items-start space-x-3 ${styles[type]} ${className}`}>
      {showIcon && (
        <Icon className={`h-5 w-5 flex-shrink-0 mt-0.5 ${iconColors[type]}`} />
      )}
      <div className="flex-1">
        <p className="text-sm">{message}</p>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className={`flex-shrink-0 ${iconColors[type]} hover:opacity-70 transition-opacity`}
        >
          <X className="h-5 w-5" />
        </button>
      )}
    </div>
  )
}

export default ErrorMessage