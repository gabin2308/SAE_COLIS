import { useEffect, useState } from "react"
import Badge from "../../components/Badge"
import { colisService } from "../../services/colisService"
import { useAuth } from "../../context/AuthContext"
import { usePermissions } from "../../hooks/usePermissions"


const STATUTS = [
  { value: "recu_universite", label: "Reçu université" },
  { value: "transfere_iut",   label: "Transféré IUT"   },
  { value: "en_attente",      label: "En attente"       },
  { value: "livre",           label: "Livré"            },
]

export default function Colis() {
  const perms = usePermissions()
  const { user } = useAuth()
  const isAdmin = user?.role === "admin"
  const [search, setSearch]             = useState("")
  const [statutFilter, setStatutFilter] = useState("all")
  const [colis, setColis]               = useState([])
  const [loading, setLoading]           = useState(true)
  const [error, setError]               = useState(null)

  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    setError(null)
    const data = isAdmin
      ? await colisService.getAll()
      : await colisService.getMesColis()

    if (!Array.isArray(data)) {
      setError("Impossible de charger les colis")
    } else {
      setColis(data)
    }
    setLoading(false)
  }

async function handleReceptionner(id) {
  const updated = await colisService.receptionner(id)
  if (!updated) { alert("Erreur lors de la réception"); return }
  // remplace uniquement le colis concerné dans le state
  setColis(prev => prev.map(c => c.id_colis === id ? updated : c))
}

  async function handleRetirer(id) {
  const updated = await colisService.retirer(id)
  if (!updated) { alert("Erreur lors du retrait"); return }
  setColis(prev => prev.map(c => c.id_colis === id ? updated : c))
}

 
async function handleDelete(id) {
  if (!window.confirm("Supprimer ce colis ?")) return
  const res = await colisService.delete(id)
  if (!res) return
  // retire le colis du state sans recharger
  setColis(prev => prev.filter(c => c.id_colis !== id))
}

  if (loading) return <p className="text-gray-500 p-6">Chargement...</p>
  if (error)   return <p className="text-red-500 p-6">{error}</p>

  const filteredColis = colis.filter(c => {
    const matchSearch =
      c.numero_suivi?.toLowerCase().includes(search.toLowerCase()) ||
      c.destinataire_nom?.toLowerCase().includes(search.toLowerCase())
    const matchStatut =
      statutFilter === "all" || c.statut_libelle === statutFilter
    return matchSearch && matchStatut
  })

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">
        {isAdmin ? "Gestion des colis" : "Mes colis"}
      </h1>

      <div className="flex gap-3 mb-4 flex-wrap">
        <input
          type="text"
          placeholder="🔎 Rechercher un colis..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm w-64"
        />

        <select
          value={statutFilter}
          onChange={(e) => setStatutFilter(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm"
        >
          <option value="all">Tous les statuts</option>
          {STATUTS.map(s => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>

        <span className="ml-auto text-sm text-gray-400 self-center">
          {filteredColis.length} colis
        </span>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left text-xs text-gray-500 uppercase">
              <tr>
                <th className="px-4 py-3">N° suivi</th>
                <th className="px-4 py-3">Destinataire</th>
                <th className="px-4 py-3">Statut</th>
                {isAdmin && <th className="px-4 py-3">Actions</th>}
              </tr>
            </thead>
            <tbody>
              {filteredColis.length === 0 ? (
                <tr>
                  <td colSpan={isAdmin ? 4 : 3} className="px-4 py-8 text-center text-gray-400">
                    Aucun colis trouvé
                  </td>
                </tr>
              ) : (
                filteredColis.map(c => (
                  <tr key={c.id_colis} className="border-t hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-xs">{c.numero_suivi ?? "—"}</td>
                    <td className="px-4 py-3">{c.destinataire_nom ?? "—"}</td>
                    <td className="px-4 py-3"><Badge statut={c.statut_libelle} /></td>

                    {isAdmin && (
                      <td className="px-4 py-3">
                        <div className="flex gap-2 flex-wrap">

                          {/* recu_universite → Réceptionner → transfere_iut */}
                          {c.statut_libelle === "recu_universite" && (
                            <button
                              onClick={() => handleReceptionner(c.id_colis)}
                              className="text-xs bg-blue-100 text-blue-600 hover:bg-blue-200 px-2 py-1 rounded"
                            >
                              ✅ Réceptionner
                            </button>
                          )}

                          {/* transfere_iut → Retirer → livre */}
                          {c.statut_libelle === "transfere_iut" && (
                            <button
                              onClick={() => handleRetirer(c.id_colis)}
                              className="text-xs bg-green-100 text-green-600 hover:bg-green-200 px-2 py-1 rounded"
                            >
                              📤 Retirer
                            </button>
                          )}

                          <button
                            onClick={() => handleDelete(c.id_colis)}
                            className="text-xs bg-red-100 text-red-600 hover:bg-red-200 px-2 py-1 rounded"
                          >
                            🗑 Supprimer
                          </button>

                        </div>
                      </td>
                    )}
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