import { createBrowserRouter, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'

export const router = createBrowserRouter([
  { path: '/',         element: <Login /> },
  { path: '/register', element: <Register /> },
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute>
        <Dashboard />
      </ProtectedRoute>
    )
  },
  { path: '*', element: <Navigate to="/" replace /> }
])