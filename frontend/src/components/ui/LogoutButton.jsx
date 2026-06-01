import { useAuth } from "../../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function LogoutButton({ showText = true }) {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
      navigate("/login")
    } catch (error) {
      console.error("Erreur lors de la déconnexion :", error)
    }
  }

  return (
    <button 
      onClick={handleLogout} 
      className="text-sm font-semibold text-rose-600 hover:text-rose-700 transition-colors flex items-center gap-1.5 p-1 rounded hover:bg-rose-50/50"
      title="Déconnexion"
    >
      <span>❌</span>
      {showText && <span className="hidden sm:inline">Déconnexion</span>}
    </button>
  )
}