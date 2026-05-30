import { useState } from "react"
import { NavLink, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

const navItems = [
  { to: "/dashboard",             icon: "🏠", label: "Tableau de bord" },
  { to: "/admin/utilisateurs",    icon: "👥", label: "Utilisateurs" },
  { to: "/admin/departements",    icon: "🏢", label: "Départements" },
  { to: "/admin/fournisseurs",    icon: "🏭", label: "Fournisseurs" },
  { to: "/admin/colis",           icon: "📦", label: "Colis" },
  { to: "/admin/bons-commande",   icon: "📋", label: "Bons de commande" },
  { to: "/admin/devis",           icon: "📄", label: "Devis" },
  { to: "/admin/demandes",        icon: "📝", label: "Demandes d'achat" },
  { to: "/admin/notifications",   icon: "🔔", label: "Notifications" },
]

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleLogout = async () => {
    await logout()
    navigate("/")
  }

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-16"
        } bg-gray-900 text-white flex flex-col transition-all duration-300 shrink-0`}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 py-5 border-b border-gray-700">
          <span className="text-2xl">📮</span>
          {sidebarOpen && (
            <span className="font-bold text-lg tracking-tight">SAE Colis</span>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto py-4">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 mx-2 rounded-lg text-sm transition-colors ${
                  isActive
                    ? "bg-indigo-600 text-white"
                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                }`
              }
            >
              <span className="text-base shrink-0">{item.icon}</span>
              {sidebarOpen && <span className="truncate">{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* User */}
        <div className="border-t border-gray-700 p-4">
          {sidebarOpen ? (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-xs font-bold shrink-0">
                {user?.full_name?.[0]?.toUpperCase() ?? "?"}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user?.full_name}</p>
                <p className="text-xs text-gray-400 truncate">{user?.role}</p>
              </div>
              <button
                onClick={handleLogout}
                className="text-gray-400 hover:text-red-400 text-xs transition-colors"
                title="Déconnexion"
              >
                ⏻
              </button>
            </div>
          ) : (
            <button
              onClick={handleLogout}
              className="w-full flex justify-center text-gray-400 hover:text-red-400 transition-colors"
              title="Déconnexion"
            >
              ⏻
            </button>
          )}
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Topbar */}
        <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-4 shrink-0">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-gray-500 hover:text-gray-800 transition-colors"
          >
            ☰
          </button>
          <h1 className="text-sm font-medium text-gray-500 flex-1">
            Bienvenue, <span className="text-gray-900 font-semibold">{user?.full_name}</span>
          </h1>
          <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full font-medium">
            {user?.role}
          </span>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}