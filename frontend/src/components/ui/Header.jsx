import { useAuth } from "../../context/AuthContext"
import { useNavigate } from "react-router-dom"
import LogoutButton from "./LogoutButton"

export default function Header({ notifCount = 0 }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  // 🚪 Fonction de gestion de la déconnexion
  const handleLogout = async () => {
    try {
      await logout() // Éteint la session (supprime le token, reset l'état user)
      navigate("/") // Redirige vers la page de connexion
    } catch (error) {
      console.error("Erreur lors de la déconnexion :", error)
    }
  }

  return (
    <header className="h-[70px] bg-white border-b border-[#dde3ec] flex items-center justify-between px-4 md:px-8 shadow-sm">
      {/* Logo / Marque */}
      <div className="flex items-center gap-4 cursor-pointer" onClick={() => navigate("/dashboard")}>
        <span className="text-xl font-bold text-[#0d4f8a] tracking-wide">CampusFret</span>
        <div className="hidden md:block bg-[#eef2f7] text-[#4a5d78] px-2.5 py-1 rounded-md text-xs font-semibold uppercase">
          {user?.role || "Utilisateur"}
        </div>
      </div>
      
      {/* Actions à droite */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <div className="relative cursor-pointer p-1" onClick={() => navigate("/notifications")}>
          <span className="text-xl">🔔</span>
          {notifCount > 0 && (
            <span className="absolute -top-1 -right-1 bg-rose-600 text-white text-[10px] font-bold rounded-full px-1.5 py-0.5 min-w-[18px] text-center">
              {notifCount}
            </span>
          )}
        </div>

        {/* Profil & Déconnexion */}
        <div className="flex items-center gap-3 border-l border-[#dde3ec] pl-4">
          <span className="text-sm font-semibold hidden sm:inline">{user?.full_name || "Profil"}</span>
          
         <LogoutButton />
        </div>
      </div>
    </header>
  )
}