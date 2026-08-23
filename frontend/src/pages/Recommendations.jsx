import { useState, useEffect } from 'react'
import { Lightbulb, Target, TrendingUp, Heart, Activity, Utensils, Moon, Droplets } from 'lucide-react'
import api from '../utils/api'

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async () => {
    try {
      const response = await api.get('/recommendations')
      setRecommendations(response.data.recommendations || [])
    } catch (error) {
      console.error('Failed to fetch recommendations:', error)
    } finally {
      setLoading(false)
    }
  }

  const categoryIcons = {
    diet: Utensils,
    exercise: Activity,
    sleep: Moon,
    hydration: Droplets,
    stress: Heart,
    screening: Target,
    lifestyle: TrendingUp,
    respiratory: Activity
  }

  const categoryColors = {
    diet: 'bg-orange-500',
    exercise: 'bg-blue-500',
    sleep: 'bg-purple-500',
    hydration: 'bg-cyan-500',
    stress: 'bg-pink-500',
    screening: 'bg-red-500',
    lifestyle: 'bg-green-500',
    respiratory: 'bg-teal-500'
  }

  const priorityColors = {
    high: 'border-red-500',
    medium: 'border-yellow-500',
    low: 'border-green-500'
  }

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
        <h1 className="text-3xl font-bold text-gray-900">Personalized Recommendations</h1>
        <p className="mt-2 text-gray-600">AI-powered health suggestions tailored for you</p>
      </div>

      {recommendations.length === 0 ? (
        <div className="card flex items-center justify-center h-96">
          <div className="text-center">
            <Lightbulb className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">
              No personalized recommendations available yet. 
              Complete your health profile to get tailored suggestions.
            </p>
          </div>
        </div>
      ) : (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card bg-gradient-to-r from-blue-50 to-blue-100">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-blue-500 rounded-lg">
                  <Activity className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Exercise</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {recommendations.filter(r => r.category === 'exercise').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-r from-orange-50 to-orange-100">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-orange-500 rounded-lg">
                  <Utensils className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Diet</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {recommendations.filter(r => r.category === 'diet').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-r from-purple-50 to-purple-100">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-purple-500 rounded-lg">
                  <Moon className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Sleep</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {recommendations.filter(r => r.category === 'sleep').length}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Recommendations List */}
          <div className="space-y-4">
            {recommendations.map((rec, idx) => {
              const Icon = categoryIcons[rec.category] || Lightbulb
              return (
                <div
                  key={idx}
                  className={`card border-l-4 ${priorityColors[rec.priority]} hover:shadow-lg transition-shadow`}
                >
                  <div className="flex items-start space-x-4">
                    <div className={`p-3 ${categoryColors[rec.category]} rounded-lg`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-semibold text-gray-900 capitalize">
                            {rec.category}
                          </h3>
                          <p className="text-gray-600 mt-1">{rec.recommendation}</p>
                        </div>
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded-full ${
                            rec.priority === 'high'
                              ? 'bg-red-100 text-red-800'
                              : rec.priority === 'medium'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-green-100 text-green-800'
                          }`}
                        >
                          {rec.priority} priority
                        </span>
                      </div>
                      {rec.reason && (
                        <p className="text-sm text-gray-500 mt-2">
                          Reason: {rec.reason}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* General Health Tips */}
          <div className="card bg-gradient-to-r from-primary-50 to-medical-50">
            <div className="flex items-start space-x-4">
              <div className="p-3 bg-medical-500 rounded-lg">
                <Lightbulb className="h-6 w-6 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">General Health Tips</h3>
                <ul className="mt-3 space-y-2">
                  <li className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-medical-600">•</span>
                    <span>Maintain a balanced diet rich in fruits and vegetables</span>
                  </li>
                  <li className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-medical-600">•</span>
                    <span>Engage in regular physical activity (150+ minutes per week)</span>
                  </li>
                  <li className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-medical-600">•</span>
                    <span>Get 7-9 hours of quality sleep each night</span>
                  </li>
                  <li className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-medical-600">•</span>
                    <span>Stay hydrated by drinking at least 8 glasses of water daily</span>
                  </li>
                  <li className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-medical-600">•</span>
                    <span>Practice stress management techniques like meditation</span>
                  </li>
                  <li className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-medical-600">•</span>
                    <span>Schedule regular health check-ups and screenings</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Recommendations
