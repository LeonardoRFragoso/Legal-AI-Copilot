import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Chat from './pages/Chat'
import Analysis from './pages/Analysis'
import Comparison from './pages/Comparison'
import RiskAnalysis from './pages/RiskAnalysis'
import Automations from './pages/Automations'
import Reviews from './pages/Reviews'
import Insights from './pages/Insights'
import { useAuthStore } from './store/authStore'

function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { user, initialized } = useAuthStore()

  if (!initialized) {
    return <div className="min-h-screen flex items-center justify-center">Carregando...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <Layout>{children}</Layout>
}

function App() {
  const { initAuth } = useAuthStore()

  useEffect(() => {
    initAuth()
  }, [initAuth])

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
        <Route path="/upload" element={<ProtectedLayout><Upload /></ProtectedLayout>} />
        <Route path="/chat" element={<ProtectedLayout><Chat /></ProtectedLayout>} />
        <Route path="/analysis" element={<ProtectedLayout><Analysis /></ProtectedLayout>} />
        <Route path="/comparison" element={<ProtectedLayout><Comparison /></ProtectedLayout>} />
        <Route path="/risks" element={<ProtectedLayout><RiskAnalysis /></ProtectedLayout>} />
        <Route path="/automations" element={<ProtectedLayout><Automations /></ProtectedLayout>} />
        <Route path="/reviews" element={<ProtectedLayout><Reviews /></ProtectedLayout>} />
        <Route path="/insights" element={<ProtectedLayout><Insights /></ProtectedLayout>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
