import { createContext, useContext, useEffect, useState } from "react"
import { authService } from "../services/authService"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 🛡️ Ajout d'un bloc .catch() pour intercepter proprement la session expirée (401)
    authService.me()
      .then(data => { 
        if (data?.id) setUser(data) 
      })
      .catch(err => {
        // L'erreur 401 levée par apiFetch est capturée ici
        console.warn("Auto-connexion impossible ou session expirée :", err.message)
        setUser(null) 
      })
      .finally(() => setLoading(false))
  }, [])

 const login = async (email, password) => {
  try {
    const data = await authService.login(email, password)
    if (data.access_token) {
      authService.saveToken(data.access_token)
      const me = await authService.me()
      setUser(me)
      return { success: true } // ✅ Important pour ton handleLogin
    }
    return { error: data.error || "Connexion échouée" }
  } catch (err) {
    return { error: err.message }
  }
}

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