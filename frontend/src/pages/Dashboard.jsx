import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  HeartPulse, 
  FileText, 
  MessageSquare, 
  Lightbulb,
  AlertCircle
} from 'lucide-react'
import api from '../utils/api'

const Dashboard = () => {
  const [stats, setStats] = useState({
    reports: 0,
    predictions: 0,
    chatMessages: 0,
    recommendations: 0
  })
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [reportsRes, predictionsRes, chatRes, recommendationsRes] = await Promise.all([
        api.get('/medical/reports').catch(() => ({ data: { reports: [] } })),
        api.get('/predict/history').catch(() => ({ data: { predictions: [] } })),
        api.get('/chat/history').catch(() => ({ data: { history: [] } })),
        api.get('/recommendations').catch(() => ({ data: { recommendations: [] } }))
      ])

      setStats({
        reports: reportsRes.data.reports?.length || 0,
        predictions: predictionsRes.data.predictions?.length || 0,
        chatMessages: chatRes.data.history?.length || 0,
        recommendations: recommendationsRes.data.recommendations?.length || 0
      })
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const quickActions = [
    {
      icon: FileText,
      title: 'Upload Medical Report',
      description: 'Analyze your medical documents with AI',
      link: '/medical-reports',
      color: 'bg-blue-500'
    },
    {
      icon: HeartPulse,
      title: 'Disease Prediction',
      description: 'Get AI-powered health risk assessment',
      link: '/prediction',
      color: 'bg-red-500'
    },
    {
      icon: MessageSquare,
      title: 'Health Chat',
      description: 'Ask health questions to AI assistant',
      link: '/chat',
      color: 'bg-green-500'
    },
    {
      icon: Lightbulb,
      title: 'Recommendations',
      description: 'Personalized health suggestions',
      link: '/recommendations',
      color: 'bg-yellow-500'
    }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Health Dashboard</h1>
        <p className="mt-2 text-gray-600">Welcome to your AI-powered health assistant</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Medical Reports</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.reports}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Predictions</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.predictions}</p>
            </div>
            <div className="p-3 bg-red-100 rounded-full">
              <HeartPulse className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Chat Messages</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.chatMessages}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <MessageSquare className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Recommendations</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.recommendations}</p>
            </div>
            <div className="p-3 bg-yellow-100 rounded-full">
              <Lightbulb className="h-6 w-6 text-yellow-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {quickActions.map((action) => {
            const Icon = action.icon
            return (
              <Link
                key={action.title}
                to={action.link}
                className="card hover:shadow-lg transition-shadow cursor-pointer group"
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-3 ${action.color} rounded-lg`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 group-hover:text-primary-600">
                      {action.title}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">{action.description}</p>
                  </div>
                </div>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Health Tips */}
      <div className="card bg-gradient-to-r from-primary-50 to-medical-50">
        <div className="flex items-start space-x-4">
          <div className="p-3 bg-medical-500 rounded-full">
            <AlertCircle className="h-6 w-6 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900">Health Reminder</h3>
            <p className="text-sm text-gray-700 mt-1">
              Remember to schedule regular check-ups with your healthcare provider. 
              Early detection is key to maintaining good health.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
