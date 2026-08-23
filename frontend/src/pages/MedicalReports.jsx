import { useState, useEffect } from 'react'
import { Upload, FileText, Calendar, AlertCircle } from 'lucide-react'
import api from '../utils/api'

const MedicalReports = () => {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)

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
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
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
      alert('Failed to upload and analyze report')
    } finally {
      setUploading(false)
    }
  }

  const handleTextAnalysis = async () => {
    const text = prompt('Enter medical report text:')
    if (!text) return

    try {
      const response = await api.post('/medical/analyze/text', { text })
      setAnalysisResult(response.data.analysis)
      fetchReports()
    } catch (error) {
      console.error('Analysis failed:', error)
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
              onClick={handleTextAnalysis}
              className="btn-secondary"
            >
              Analyze Text
            </button>
          </div>
        </div>
      </div>

      {/* Analysis Result */}
      {analysisResult && (
        <div className="card bg-gradient-to-r from-primary-50 to-medical-50">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Result</h2>
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
