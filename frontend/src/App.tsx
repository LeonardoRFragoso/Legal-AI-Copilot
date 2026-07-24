import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Chat from './pages/Chat'
import Analysis from './pages/Analysis'
import Comparison from './pages/Comparison'
import RiskAnalysis from './pages/RiskAnalysis'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/comparison" element={<Comparison />} />
          <Route path="/risks" element={<RiskAnalysis />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
