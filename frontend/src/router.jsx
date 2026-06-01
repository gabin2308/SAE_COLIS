import { createBrowserRouter, Navigate } from 'react-router-dom'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Dashboard from './pages/lecteur/Dashboard'
import Demande from './pages/lecteur/Demande'
import Colis from './pages/lecteur/Colis'
import { useAuth } from './context/AuthContext'
import DevisManager from './pages/lecteur/Devis'


const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()
  if (loading) return <div>Chargement...</div>
  return user ? children : <Navigate to="/login" replace />
}


const PublicOnlyRoute = ({ children }) => {
  const { user, loading } = useAuth()
  if (loading) return <div>Chargement...</div>
  return !user ? children : <Navigate to="/dashboard" replace />
}

export default createBrowserRouter([
  { path: '/login', element: <PublicOnlyRoute><Login /></PublicOnlyRoute> },
  { path: '/register', element: <PublicOnlyRoute><Register /></PublicOnlyRoute> },
  { path: '/dashboard', element: <ProtectedRoute><Dashboard /></ProtectedRoute> },
  { path: '/demande', element: <ProtectedRoute><Demande /></ProtectedRoute> },
  { path: '/colis', element: <ProtectedRoute><Colis /></ProtectedRoute> },
  { path: '/devis', element: <ProtectedRoute><DevisManager /></ProtectedRoute> },
  { path: '*', element: <Navigate to="/dashboard" replace /> }
])