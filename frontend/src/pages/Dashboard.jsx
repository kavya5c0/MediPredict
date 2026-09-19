import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  HeartPulse, 
  FileText, 
  MessageSquare, 
  Lightbulb,
  AlertCircle,
  TrendingUp,
  Activity,
  Shield
} from 'lucide-react'
import api, { quietApi } from '../utils/api'
import StatCard from '../components/StatCard'
import HealthOverviewChart from '../components/charts/HealthOverviewChart'
import HealthTrendChart from '../components/charts/HealthTrendChart'
import DiseaseRiskChart from '../components/charts/DiseaseRiskChart'
import HealthGaugeChart from '../components/charts/HealthGaugeChart'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

const Dashboard = () => {
  const [stats, setStats] = useState({
    reports: 0,
    predictions: 0,
    chatMessages: 0,
    recommendations: 0
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [reportsRes, predictionsRes, chatRes, recommendationsRes] = await Promise.all([
        quietApi.get('/medical/reports').catch(() => ({ data: { reports: [] } })),
        quietApi.get('/predict/history').catch(() => ({ data: { predictions: [] } })),
        quietApi.get('/chat/history').catch(() => ({ data: { history: [] } })),
        quietApi.get('/recommendations').catch(() => ({ data: { recommendations: [] } }))
      ])

      setStats({
        reports: reportsRes.data.reports?.length || 0,
        predictions: predictionsRes.data.predictions?.length || 0,
        chatMessages: chatRes.data.history?.length || 0,
        recommendations: recommendationsRes.data.recommendations?.length || 0
      })
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      setError('Failed to load dashboard data. Please refresh the page.')
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
      color: 'from-blue-500 to-blue-600',
      iconColor: 'blue'
    },
    {
      icon: HeartPulse,
      title: 'Disease Prediction',
      description: 'Get AI-powered health risk assessment',
      link: '/prediction',
      color: 'from-red-500 to-red-600',
      iconColor: 'red'
    },
    {
      icon: MessageSquare,
      title: 'Health Chat',
      description: 'Ask health questions to AI assistant',
      link: '/chat',
      color: 'from-green-500 to-green-600',
      iconColor: 'green'
    },
    {
      icon: Lightbulb,
      title: 'Recommendations',
      description: 'Personalized health suggestions',
      link: '/recommendations',
      color: 'from-yellow-500 to-yellow-600',
      iconColor: 'yellow'
    }
  ]

  if (loading) {
    return <LoadingSpinner size="lg" text="Loading your health data..." fullScreen={true} />
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <ErrorMessage 
          message={error} 
          type="error"
          onDismiss={() => setError(null)}
        />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Health Dashboard</h1>
        <p className="mt-2 text-gray-600">Welcome to your AI-powered health assistant</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Medical Reports" 
          value={stats.reports} 
          icon={FileText} 
          color="blue"
        />
        <StatCard 
          title="Predictions" 
          value={stats.predictions} 
          icon={HeartPulse} 
          color="red"
        />
        <StatCard 
          title="Chat Messages" 
          value={stats.chatMessages} 
          icon={MessageSquare} 
          color="green"
        />
        <StatCard 
          title="Recommendations" 
          value={stats.recommendations} 
          icon={Lightbulb} 
          color="yellow"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Activity className="h-5 w-5 mr-2 text-primary-600" />
              Health Overview
            </h3>
          </div>
          <HealthOverviewChart stats={stats} />
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-primary-600" />
              Health Trends
            </h3>
          </div>
          <HealthTrendChart />
        </div>
      </div>

      {/* Risk and Health Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Shield className="h-5 w-5 mr-2 text-primary-600" />
              Disease Risk Analysis
            </h3>
          </div>
          <DiseaseRiskChart />
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Health Score</h3>
          </div>
          <HealthGaugeChart value={78} title="Score" />
          <p className="text-center text-sm text-gray-600 mt-4">Based on your recent health data</p>
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
                  <div className={`p-3 bg-gradient-to-br ${action.color} rounded-lg`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
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
      <div className="card bg-gradient-to-r from-primary-500 to-medical-500 text-white">
        <div className="flex items-start space-x-4">
          <div className="p-3 bg-white/20 rounded-full">
            <AlertCircle className="h-6 w-6 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-white text-lg">Health Reminder</h3>
            <p className="text-sm text-white/90 mt-2">
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
