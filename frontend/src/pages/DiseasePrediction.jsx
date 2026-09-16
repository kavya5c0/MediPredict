import { useState } from 'react'
import { HeartPulse, AlertTriangle, TrendingUp, Activity } from 'lucide-react'
import api from '../utils/api'

const DiseasePrediction = () => {
  const [healthData, setHealthData] = useState({
    age: '',
    bmi: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    heart_rate: '',
    glucose_level: '',
    cholesterol: '',
    smoking: false,
    alcohol: false,
    family_history_diabetes: false,
    family_history_heart: false,
    family_history_hypertension: false,
    physical_activity: '',
    sleep_hours: '',
    stress_level: '',
    diabetes: false,
    heart_disease: false,
    hypertension: false,
    asthma: false,
    arthritis: false
  })
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setHealthData({
      ...healthData,
      [name]: type === 'checkbox' ? checked : value
    })
  }

  const handlePredict = async () => {
    setLoading(true)
    try {
      const response = await api.post('/predict/disease', healthData)
      setPrediction(response.data)
    } catch (error) {
      console.error('Prediction failed:', error)
      alert('Failed to get prediction: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Disease Prediction</h1>
        <p className="mt-2 text-gray-600">AI-powered health risk assessment</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Health Data Form */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Health Information</h2>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                <input
                  type="number"
                  name="age"
                  value={healthData.age}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="25"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">BMI</label>
                <input
                  type="number"
                  step="0.1"
                  name="bmi"
                  value={healthData.bmi}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="24.5"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Blood Pressure (Systolic)</label>
                <input
                  type="number"
                  name="blood_pressure_systolic"
                  value={healthData.blood_pressure_systolic}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="120"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Blood Pressure (Diastolic)</label>
                <input
                  type="number"
                  name="blood_pressure_diastolic"
                  value={healthData.blood_pressure_diastolic}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="80"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Heart Rate</label>
                <input
                  type="number"
                  name="heart_rate"
                  value={healthData.heart_rate}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="72"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Glucose Level</label>
                <input
                  type="number"
                  name="glucose_level"
                  value={healthData.glucose_level}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="100"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Cholesterol</label>
              <input
                type="number"
                name="cholesterol"
                value={healthData.cholesterol}
                onChange={handleChange}
                className="input-field"
                placeholder="200"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Physical Activity (min/week)</label>
                <input
                  type="number"
                  name="physical_activity"
                  value={healthData.physical_activity}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="150"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sleep Hours</label>
                <input
                  type="number"
                  name="sleep_hours"
                  value={healthData.sleep_hours}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="7"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Stress Level (1-10)</label>
              <input
                type="number"
                name="stress_level"
                value={healthData.stress_level}
                onChange={handleChange}
                className="input-field"
                placeholder="5"
                min="1"
                max="10"
              />
            </div>

            <div className="border-t pt-4">
              <h3 className="font-medium text-gray-900 mb-3">Lifestyle Factors</h3>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="smoking"
                    checked={healthData.smoking}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Smoking</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="alcohol"
                    checked={healthData.alcohol}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Alcohol Consumption</span>
                </label>
              </div>
            </div>

            <div className="border-t pt-4">
              <h3 className="font-medium text-gray-900 mb-3">Family History</h3>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="family_history_diabetes"
                    checked={healthData.family_history_diabetes}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Diabetes</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="family_history_heart"
                    checked={healthData.family_history_heart}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Heart Disease</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="family_history_hypertension"
                    checked={healthData.family_history_hypertension}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Hypertension</span>
                </label>
              </div>
            </div>

            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Get Prediction'}
            </button>
          </div>
        </div>

        {/* Prediction Results */}
        <div className="space-y-6">
          {prediction ? (
            <>
              <div className="card bg-gradient-to-r from-primary-50 to-medical-50">
                <div className="flex items-center space-x-3 mb-4">
                  <Activity className="h-6 w-6 text-primary-600" />
                  <h2 className="text-lg font-semibold text-gray-900">Prediction Results</h2>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Primary Risk</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {prediction.predicted_disease}
                    </p>
                    <p className="text-sm text-gray-600">
                      Confidence: {(prediction.confidence * 100).toFixed(1)}%
                    </p>
                  </div>

                  <div>
                    <h3 className="font-medium text-gray-700 mb-2">Risk Factors</h3>
                    <div className="space-y-2">
                      {prediction.risk_factors?.map((factor, idx) => (
                        <div key={idx} className="flex items-center space-x-2">
                          <AlertTriangle className="h-4 w-4 text-yellow-600" />
                          <span className="text-sm text-gray-600">{factor}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h3 className="font-medium text-gray-700 mb-2">Recommendations</h3>
                    <ul className="list-disc list-inside space-y-1">
                      {prediction.recommendations?.map((rec, idx) => (
                        <li key={idx} className="text-sm text-gray-600">{rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="font-medium text-gray-900 mb-4">All Disease Probabilities</h3>
                <div className="space-y-3">
                  {Object.entries(prediction.all_probabilities)
                    .sort(([, a], [, b]) => b - a)
                    .map(([disease, prob]) => (
                      <div key={disease}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{disease}</span>
                          <span className="text-gray-600">{(prob * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${prob * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </>
          ) : (
            <div className="card flex items-center justify-center h-96">
              <div className="text-center">
                <HeartPulse className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">
                  Fill in your health information and click "Get Prediction" 
                  to see your risk assessment
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DiseasePrediction
