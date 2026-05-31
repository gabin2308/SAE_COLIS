import { createContext, useContext, useEffect, useState } from "react"
import { authService } from "../services/authService"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    authService.me()
      .then(data => { if (data?.id) setUser(data) })
      .finally(() => setLoading(false))
  }, [])

  const login = async (email, password) => {
    const data = await authService.login(email, password)
    if (data.access_token) {
      authService.saveToken(data.access_token)
      const me = await authService.me()
      setUser(me)
      return { success: true }
    }
    return { error: data.error }
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