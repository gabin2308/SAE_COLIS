import { useEffect, useState } from "react"
import { colisService } from "../../services/colisService"

function Badge({ statut }) {
  const map = {
    recu_universite: "bg-blue-100 text-blue-700",
    transfere_iut:   "bg-indigo-100 text-indigo-700",
    en_attente:      "bg-yellow-100 text-yellow-700",
    livre:           "bg-green-100 text-green-700",
    probleme:        "bg-red-100 text-red-700",
  }
  const labels = {
    recu_universite: "Reçu université",
    transfere_iut:   "Transféré IUT",
    en_attente:      "En attente",
    livre:           "Livré",
    probleme:        "Problème",
  }
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${map[statut] ?? "bg-gray-100 text-gray-500"}`}>
      {labels[statut] ?? statut?.replace(/_/g, " ") ?? "—"}
    </span>
  )
}

export default function MesColis() {
  const [colis, setColis]       = useState([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [search, setSearch]     = useState("")
  const [statutFilter, setStatutFilter] = useState("all")

  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    setError(null)
    const data = await colisService.getMesColis()
    if (!Array.isArray(data)) {
      setError("Impossible de charger vos colis")
    } else {
      setColis(data)
    }
    setLoading(false)
  }

  if (loading) return <p className="text-gray-500 p-6">Chargement...</p>
  if (error)   return <p className="text-red-500 p-6">{error}</p>

  const filtered = colis.filter(c => {
    const matchSearch =
      c.numero_suivi?.toLowerCase().includes(search.toLowerCase()) ||
      c.commentaire?.toLowerCase().includes(search.toLowerCase())
    const matchStatut = statutFilter === "all" || c.statut_libelle === statutFilter
    return matchSearch && matchStatut
  })

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Mes colis</h1>
        <p className="text-sm text-gray-500 mt-1">Suivez l'état de vos colis</p>
      </div>

      <div className="flex gap-3 mb-4 flex-wrap">
        <input
          type="text"
          placeholder="🔎 Rechercher un colis..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm w-64"
        />
        <select
          value={statutFilter}
          onChange={e => setStatutFilter(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm"
        >
          <option value="all">Tous les statuts</option>
          <option value="recu_universite">Reçu université</option>
          <option value="transfere_iut">Transféré IUT</option>
          <option value="en_attente">En attente</option>
          <option value="livre">Livré</option>
          <option value="probleme">Problème</option>
        </select>
        <span className="ml-auto text-sm text-gray-400 self-center">
          {filtered.length} colis
        </span>
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
          <p className="text-4xl mb-3">📦</p>
          <p className="text-gray-500 text-sm">Aucun colis trouvé</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(c => (
            <div
              key={c.id_colis}
              className="bg-white rounded-xl border border-gray-100 shadow-sm p-5"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center text-xl shrink-0">
                    📦
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 font-mono text-sm">
                      {c.numero_suivi ?? "—"}
                    </p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {c.commentaire ?? "Aucun commentaire"}
                    </p>
                  </div>
                </div>
                <Badge statut={c.statut_libelle} />
              </div>

              <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs text-gray-500">
                <div>
                  <p className="text-gray-400 uppercase tracking-wide mb-0.5">Réception</p>
                  <p className="text-gray-700">{c.date_reception ?? "—"}</p>
                </div>
                <div>
                  <p className="text-gray-400 uppercase tracking-wide mb-0.5">Retrait</p>
                  <p className="text-gray-700">{c.date_retrait ?? "—"}</p>
                </div>
                <div>
                  <p className="text-gray-400 uppercase tracking-wide mb-0.5">Code-barres</p>
                  <p className="text-gray-700 font-mono">{c.code_barres ?? "—"}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}