import { createContext, useContext, useEffect, useState } from "react"
import { authService } from "../services/authService"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Initialisation : Vérification du token au chargement
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem("token")
      
      // Si aucun token, on arrête le chargement immédiatement
      if (!token) {
        setLoading(false)
        return
      }

      try {
        const data = await authService.me()
        if (data?.id) {
          setUser(data)
        } else {
          // Token invalide ou expiré
          authService.clearAuth()
        }
      } catch (err) {
        console.warn("Session expirée :", err.message)
        authService.clearAuth()
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    initAuth()
  }, [])

  // Fonction login mise à jour
  const login = async (email, password) => {
    try {
      const data = await authService.login(email, password)
      
      if (data?.access_token) {
        authService.saveToken(data.access_token)
        // Récupérer le profil après succès
        const me = await authService.me()
        setUser(me)
        return { success: true }
      }
      
      return { error: data?.error || "Identifiants invalides" }
    } catch (err) {
      return { error: err.message || "Erreur de connexion serveur" }
    }
  }

  // Fonction logout
  const logout = () => {
    authService.logout()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)