import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { userService } from "../../services/UtilisateurService"
import { Loader2, Trash2, UserPlus, ArrowLeft } from "lucide-react"
import Header from "../../components/ui/Header"

export default function Utilisateur() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    try {
      setLoading(true)
      const data = await userService.getAll()
      // On s'assure que data est bien un tableau
      setUsers(Array.isArray(data) ? data : [])
    } catch (err) {
      setError("Erreur lors du chargement : " + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id_utilisateur) => {
    if (!window.confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?")) return

    try {
      await userService.delete(id_utilisateur)
      // Utilisation de id_utilisateur au lieu de id pour correspondre à votre classe Python
      setUsers(users.filter((user) => user.id_utilisateur !== id_utilisateur))
    } catch (err) {
      alert("Erreur lors de la suppression : " + err.message)
    }
  }

  return (
    <div className="min-h-screen bg-[#f7f9fc]">
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-8">
        
        {/* En-tête de page */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate("/dashboard")}
              className="text-slate-400 hover:text-[#0d2a4a] text-sm font-medium flex items-center gap-1"
            >
              <ArrowLeft size={16} /> Retour
            </button>
            <h1 className="text-2xl font-bold text-[#0d2a4a]">Gestion des utilisateurs</h1>
          </div>
          <button
            onClick={() => navigate("/utilisateurs/ajouter")}
            className="flex items-center gap-2 bg-[#0d4f8a] text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-[#0a3d6b] transition-colors"
          >
            <UserPlus size={16} /> Ajouter un utilisateur
          </button>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-xl border border-red-200 mb-6 text-sm">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="animate-spin text-[#0d4f8a]" size={36} />
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-4 font-medium text-slate-500">Nom complet</th>
                  <th className="px-6 py-4 font-medium text-slate-500">Email</th>
                  <th className="px-6 py-4 font-medium text-slate-500">Rôle</th>
                  <th className="px-6 py-4 font-medium text-slate-500 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((user) => (
                  <tr key={user.id_utilisateur} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-medium text-[#0d2a4a]">{user.fullName}</td>
                    <td className="px-6 py-4 text-slate-600">{user.email}</td>
                    <td className="px-6 py-4 text-slate-600">
                      <span className="bg-slate-100 px-2 py-1 rounded text-xs font-medium">
                        {user.role_nom || "Non défini"}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button 
                        onClick={() => handleDelete(user.id_utilisateur)}
                        className="text-red-600 hover:bg-red-50 p-2 rounded-lg transition-colors"
                        title="Supprimer"
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  )
}