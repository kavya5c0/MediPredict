import { useState, useEffect } from 'react'
import { Upload, FileText, Calendar, AlertCircle, X, FileSearch } from 'lucide-react'
import api from '../utils/api'

const MedicalReports = () => {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [showTextAnalysis, setShowTextAnalysis] = useState(false)
  const [analysisText, setAnalysisText] = useState('')
  const [analyzingText, setAnalyzingText] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const response = await api.get('/medical/reports')
      setReports(response.data.reports || [])
    } catch (error) {
      console.error('Failed to fetch reports:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0])
    setError(null)
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
    setError(null)
    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await api.post('/medical/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setAnalysisResult(response.data.analysis)
      fetchReports()
      setSelectedFile(null)
    } catch (error) {
      console.error('Upload failed:', error)
      setError('Failed to upload and analyze report: ' + (error.response?.data?.detail || error.message))
    } finally {
      setUploading(false)
    }
  }

  const handleTextAnalysis = async () => {
    if (!analysisText.trim()) {
      setError('Please enter medical report text to analyze')
      return
    }

    setAnalyzingText(true)
    setError(null)

    try {
      const response = await api.post('/medical/analyze/text', { text: analysisText })
      setAnalysisResult(response.data.analysis)
      fetchReports()
      setAnalysisText('')
      setShowTextAnalysis(false)
    } catch (error) {
      console.error('Analysis failed:', error)
      setError('Failed to analyze text: ' + (error.response?.data?.detail || error.message))
    } finally {
      setAnalyzingText(false)
    }
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
        <h1 className="text-3xl font-bold text-gray-900">Medical Reports</h1>
        <p className="mt-2 text-gray-600">Upload and analyze your medical documents</p>
      </div>

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
            <X className="h-5 w-5" />
          </button>
        </div>
      )}

      {/* Upload Section */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Report</h2>
        
        <div className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-500 transition-colors">
            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-sm text-gray-600 mb-4">
              Drag and drop a file, or click to select
            </p>
            <input
              type="file"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
              accept="image/*,.pdf"
            />
            <label
              htmlFor="file-upload"
              className="btn-secondary cursor-pointer inline-block"
            >
              Select File
            </label>
            {selectedFile && (
              <p className="mt-2 text-sm text-gray-700">
                Selected: {selectedFile.name}
              </p>
            )}
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Analyzing...' : 'Upload & Analyze'}
            </button>
            <button
              onClick={() => setShowTextAnalysis(!showTextAnalysis)}
              className="btn-secondary flex items-center space-x-2"
            >
              <FileSearch className="h-4 w-4" />
              <span>{showTextAnalysis ? 'Hide' : 'Analyze'} Text</span>
            </button>
          </div>
        </div>
      </div>

      {/* Text Analysis Form */}
      {showTextAnalysis && (
        <div className="card bg-gray-50">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Analyze Medical Text</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="analysis-text" className="block text-sm font-medium text-gray-700 mb-2">
                Enter medical report text
              </label>
              <textarea
                id="analysis-text"
                value={analysisText}
                onChange={(e) => setAnalysisText(e.target.value)}
                placeholder="Paste your medical report text here..."
                rows={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 resize-none"
              />
              <p className="mt-1 text-xs text-gray-500">
                {analysisText.length} characters
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={handleTextAnalysis}
                disabled={!analysisText.trim() || analyzingText}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {analyzingText ? 'Analyzing...' : 'Analyze Text'}
              </button>
              <button
                onClick={() => {
                  setShowTextAnalysis(false)
                  setAnalysisText('')
                  setError(null)
                }}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Analysis Result */}
      {analysisResult && (
        <div className="card bg-gradient-to-r from-primary-50 to-medical-50">
          <div className="flex items-start justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Analysis Result</h2>
            <button 
              onClick={() => setAnalysisResult(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-gray-700 mb-2">Summary</h3>
              <p className="text-gray-600">{analysisResult.summary}</p>
            </div>
            
            {analysisResult.medical_entities && (
              <div>
                <h3 className="font-medium text-gray-700 mb-2">Detected Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  {analysisResult.medical_entities.diseases?.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-red-600">Conditions:</p>
                      <p className="text-sm text-gray-600">
                        {analysisResult.medical_entities.diseases.join(', ')}
                      </p>
                    </div>
                  )}
                  {analysisResult.medical_entities.medications?.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-blue-600">Medications:</p>
                      <p className="text-sm text-gray-600">
                        {analysisResult.medical_entities.medications.join(', ')}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {analysisResult.recommendations?.length > 0 && (
              <div>
                <h3 className="font-medium text-gray-700 mb-2">Recommendations</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysisResult.recommendations.map((rec, idx) => (
                    <li key={idx} className="text-sm text-gray-600">{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Reports List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Reports</h2>
        
        {reports.length === 0 ? (
          <div className="text-center py-8">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No reports uploaded yet</p>
          </div>
        ) : (
          <div className="space-y-3">
            {reports.map((report) => (
              <div
                key={report._id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <FileText className="h-5 w-5 text-primary-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{report.filename}</p>
                    <p className="text-sm text-gray-600">
                      {new Date(report.uploaded_at || report.analyzed_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <Calendar className="h-5 w-5 text-gray-400" />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default MedicalReports
