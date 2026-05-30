import { useEffect, useState } from "react"
import { adminUserService } from "../../services/adminUserService"

const ROLES = [
  { value: "admin",        label: "Admin"        },
  { value: "postal_iut",   label: "Postal IUT"   },
  { value: "postal_univ",  label: "Postal Univ"  },
  { value: "finance",      label: "Finance"      },
  { value: "directeur",    label: "Directeur"    },
  { value: "departement",  label: "Département"  },
  { value: "lecteur",      label: "Lecteur"      },
]

function Badge({ role, libelle }) {
  const styles = {
    admin:            "bg-blue-100 text-blue-700",
    chef_departement: "bg-purple-100 text-purple-700",
    user:             "bg-gray-100 text-gray-600",
  }
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${styles[role] ?? styles.user}`}>
      {libelle}
    </span>
  )
}

function Avatar({ name }) {
  const initials = name?.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase() ?? "?"
  return (
    <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-medium shrink-0">
      {initials}
    </div>
  )
}

export default function Utilisateurs() {
  const [users, setUsers]           = useState([])
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [search, setSearch]         = useState("")
  const [roleFilter, setRoleFilter] = useState("all")

  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    setError(null)
    const data = await adminUserService.getAll()
    if (!Array.isArray(data)) {
      setError(data?.error || "Impossible de charger les utilisateurs")
    } else {
      setUsers(data)
    }
    setLoading(false)
  }

  async function handleDelete(id, name) {
    if (!window.confirm(`Supprimer ${name} ?`)) return
    const res = await adminUserService.delete(id)
    if (res?.error) { alert(res.error); return }
    setUsers(prev => prev.filter(u => u.id_utilisateur !== id))
  }

  if (loading) return <p className="text-gray-500 p-6">Chargement...</p>
  if (error)   return <p className="text-red-500 p-6">{error}</p>

  const filtered = users.filter(u => {
    const matchSearch =
      u.full_name?.toLowerCase().includes(search.toLowerCase()) ||
      u.email?.toLowerCase().includes(search.toLowerCase())
    const matchRole = roleFilter === "all" || u.role === roleFilter
    return matchSearch && matchRole
  })

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Gestion des utilisateurs</h1>

      <div className="flex gap-3 mb-4 flex-wrap">
        <input
          type="text"
          placeholder="🔎 Rechercher un utilisateur..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm w-64"
        />

        <select
          value={roleFilter}
          onChange={e => setRoleFilter(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm"
        >
          <option value="all">Tous les rôles</option>
          {ROLES.map(r => (
            <option key={r.value} value={r.value}>{r.label}</option>
          ))}
        </select>

        <span className="ml-auto text-sm text-gray-400 self-center">
          {filtered.length} utilisateur{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left text-xs text-gray-500 uppercase">
              <tr>
                <th className="px-4 py-3">Utilisateur</th>
                <th className="px-4 py-3">Email</th>
                <th className="px-4 py-3">Rôle</th>
                <th className="px-4 py-3">Département</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-gray-400">
                    Aucun utilisateur trouvé
                  </td>
                </tr>
              ) : (
                filtered.map(u => (
                  <tr key={u.id_utilisateur} className="border-t hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <Avatar name={u.full_name} />
                        <span className="font-medium">{u.full_name ?? "—"}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-gray-500">{u.email ?? "—"}</td>
                    <td className="px-4 py-3">
                      <Badge role={u.role} libelle={u.role_libelle ?? u.role} />
                    </td>
                    <td className="px-4 py-3 text-gray-500">{u.departement_nom ?? "—"}</td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2 flex-wrap">
                        <button
                          onClick={() => {/* ouvrir modal édition */}}
                          className="text-xs bg-blue-100 text-blue-600 hover:bg-blue-200 px-2 py-1 rounded"
                        >
                          ✏️ Modifier
                        </button>
                        <button
                          onClick={() => {/* ouvrir modal mot de passe */}}
                          className="text-xs bg-green-100 text-green-600 hover:bg-green-200 px-2 py-1 rounded"
                        >
                          🔑 MDP
                        </button>
                        <button
                          onClick={() => handleDelete(u.id_utilisateur, u.full_name)}
                          className="text-xs bg-red-100 text-red-600 hover:bg-red-200 px-2 py-1 rounded"
                        >
                          🗑 Supprimer
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}