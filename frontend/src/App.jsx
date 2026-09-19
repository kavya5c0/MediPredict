import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import MedicalReports from './pages/MedicalReports'
import DiseasePrediction from './pages/DiseasePrediction'
import HealthChat from './pages/HealthChat'
import Recommendations from './pages/Recommendations'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="medical-reports" element={<MedicalReports />} />
          <Route path="prediction" element={<DiseasePrediction />} />
          <Route path="chat" element={<HealthChat />} />
          <Route path="recommendations" element={<Recommendations />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
