import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate("/")
  }

  return (
    <div>
      <h1>Bienvenue {user?.full_name}</h1>
      <p>Rôle : {user?.role}</p>
      <button onClick={handleLogout}>Se déconnecter</button>
    </div>
  )
}