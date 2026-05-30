import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth()

  if (loading) return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", background: "#0a0a0f", color: "#7cf5c8", fontFamily: "monospace" }}>
      Chargement...
    </div>
  )

  if (!user) return <Navigate to="/" replace />

  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />

  return children
}