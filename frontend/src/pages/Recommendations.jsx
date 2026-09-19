import { useState, useEffect } from 'react'
import { Lightbulb, Target, TrendingUp, Heart, Activity, Utensils, Moon, Droplets, ChevronDown, ChevronUp, AlertCircle } from 'lucide-react'
import api from '../utils/api'
import LoadingSpinner from '../components/LoadingSpinner'

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [showProfileForm, setShowProfileForm] = useState(false)
  const [submittingProfile, setSubmittingProfile] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  
  const [profileData, setProfileData] = useState({
    age: '',
    gender: '',
    conditions: '',
    activity_level: '',
    smoking: false
  })

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

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    setSubmittingProfile(true)
    setError(null)
    setSuccess(null)

    try {
      // Parse conditions from comma-separated string to array
      const profilePayload = {
        age: parseInt(profileData.age),
        gender: profileData.gender,
        conditions: profileData.conditions.split(',').map(c => c.trim()).filter(c => c),
        activity_level: profileData.activity_level,
        smoking: profileData.smoking
      }

      await api.post('/recommendations/profile', profilePayload)
      setSuccess('Health profile updated successfully!')
      setShowProfileForm(false)
      
      // Re-fetch recommendations with updated profile
      setLoading(true)
      await fetchRecommendations()
    } catch (error) {
      console.error('Failed to update profile:', error)
      setError('Failed to update health profile: ' + (error.response?.data?.detail || error.message))
    } finally {
      setSubmittingProfile(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setProfileData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
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
    return <LoadingSpinner size="lg" text="Loading your recommendations..." fullScreen={false} />
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Personalized Recommendations</h1>
          <p className="mt-2 text-gray-600">AI-powered health suggestions tailored for you</p>
        </div>
        <button
          onClick={() => setShowProfileForm(!showProfileForm)}
          className="btn-primary flex items-center space-x-2"
        >
          {showProfileForm ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          <span>Health Profile</span>
        </button>
      </div>

      {/* Success Message */}
      {success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start space-x-3">
          <Lightbulb className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm text-green-800">{success}</p>
          </div>
          <button 
            onClick={() => setSuccess(null)}
            className="text-green-600 hover:text-green-800"
          >
            ×
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm text-red-800">{error}</p>
          </div>
          <button 
            onClick={() => setError(null)}
            className="text-red-600 hover:text-red-800"
          >
            ×
          </button>
        </div>
      )}

      {/* Health Profile Form */}
      {showProfileForm && (
        <div className="card bg-gray-50">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Update Health Profile</h2>
          <form onSubmit={handleProfileSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="age" className="block text-sm font-medium text-gray-700 mb-1">
                  Age
                </label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={profileData.age}
                  onChange={handleInputChange}
                  min="1"
                  max="120"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                />
              </div>

              <div>
                <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-1">
                  Gender
                </label>
                <select
                  id="gender"
                  name="gender"
                  value={profileData.gender}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label htmlFor="activity_level" className="block text-sm font-medium text-gray-700 mb-1">
                  Activity Level
                </label>
                <select
                  id="activity_level"
                  name="activity_level"
                  value={profileData.activity_level}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="">Select activity level</option>
                  <option value="sedentary">Sedentary (little or no exercise)</option>
                  <option value="moderate">Moderate (exercise 1-3 days/week)</option>
                  <option value="active">Active (exercise 3-5 days/week)</option>
                  <option value="very_active">Very Active (exercise 6-7 days/week)</option>
                </select>
              </div>

              <div>
                <label htmlFor="conditions" className="block text-sm font-medium text-gray-700 mb-1">
                  Medical Conditions
                </label>
                <input
                  type="text"
                  id="conditions"
                  name="conditions"
                  value={profileData.conditions}
                  onChange={handleInputChange}
                  placeholder="e.g., diabetes, hypertension"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                />
                <p className="mt-1 text-xs text-gray-500">Separate multiple conditions with commas</p>
              </div>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="smoking"
                name="smoking"
                checked={profileData.smoking}
                onChange={handleInputChange}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="smoking" className="ml-2 block text-sm text-gray-700">
                I am a smoker
              </label>
            </div>

            <div className="flex space-x-3 pt-2">
              <button
                type="submit"
                disabled={submittingProfile}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submittingProfile ? 'Saving...' : 'Save Profile'}
              </button>
              <button
                type="button"
                onClick={() => setShowProfileForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {recommendations.length === 0 ? (
        <div className="card flex items-center justify-center h-96">
          <div className="text-center">
            <Lightbulb className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">
              No personalized recommendations available yet.
            </p>
            <button
              onClick={() => setShowProfileForm(true)}
              className="btn-primary"
            >
              Complete Health Profile
            </button>
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
