import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-950 text-emerald-300">
        Chargement...
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/" replace />
  }

  if (roles && !roles.includes(user.role)) {

    switch (user.role) {
      case "departement":
        return <Navigate to="/departement" replace />

      case "postal_iut":
        return <Navigate to="/postal_iut" replace />

      case "directeur":
        return <Navigate to="/directeur" replace />

      case "postal_univ":
        return <Navigate to ="/postal_univ" replace/> 
        
      case "finance":
        return <Navigate to="/finance" replace/>  

      case "lecteur":
        return <Navigate to="/lecteur" replace/>
    
      default:
        return <Navigate to="/" replace />
    }
  }

  return children
}