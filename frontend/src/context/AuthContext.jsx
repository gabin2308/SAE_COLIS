import { createContext, useContext, useEffect, useState } from "react"
import { authService } from "../services/authService"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    authService.me()
      .then(data => { if (data.id) setUser(data) })
      .finally(() => setLoading(false))
  }, [])

  const login  = (userData) => setUser(userData)
  const logout = async () => {
    await authService.logout()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)