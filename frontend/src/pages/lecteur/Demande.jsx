import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { demandeService } from "../../services/demandeService"
import { useAuth } from "../../context/AuthContext"
import StatusBadge from "../../components/ui/StatusBadge"
import Header from "../../components/ui/Header"
import { Search, Filter, Loader2, RefreshCw, Plus } from "lucide-react"

const STATUTS = [
  { value: "tous",       label: "Tous les statuts" },
  { value: "en_attente", label: "En attente" },
  { value: "approuvee",  label: "Approuvée" },
  { value: "refusee",    label: "Refusée" },
]

export default function Demandes() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [demandes, setDemandes] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(null)

  const [search, setSearch] = useState("")
  const [filter, setFilter] = useState("tous")

  const isAdmin = user?.role === "administrateur"

  const fetchData = async () => {
    setLoading(true)
    try {
      const data = isAdmin
        ? await demandeService.getAll()
        : await demandeService.getMesDemandes()
      setDemandes(data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [])

  const handleAction = async (id, action) => {
    setActionLoading(id)
    try {
      if (action === "approuve") await demandeService.approuver(id)
      else                       await demandeService.refuser(id)
      await fetchData()
    } catch (err) {
      alert("Erreur lors de la mise à jour du statut.")
      console.error(err)
    } finally {
      setActionLoading(null)
    }
  }

  const processed = useMemo(() => {
    return demandes
      .filter(d => {
        const q = search.trim().toLowerCase()
        const matchSearch = !q ||
          d.objet?.toLowerCase().includes(q) ||
          d.description?.toLowerCase().includes(q) ||
          d.demandeur_nom?.toLowerCase().includes(q)
        const matchStatus = filter === "tous" || d.statut === filter
        return matchSearch && matchStatus
      })
      .sort((a, b) => new Date(b.date_creation || 0) - new Date(a.date_creation || 0))
  }, [demandes, search, filter])

  const resetFiltres = () => {
    setSearch("")
    setFilter("tous")
  }

  const formatDate = (d) => d ? new Date(d).toLocaleDateString("fr-FR") : "—"

  const stats = useMemo(() => ({
    total:      demandes.length,
    en_attente: demandes.filter(d => d.statut === "en_attente").length,
    approuvee:  demandes.filter(d => d.statut === "approuvee").length,
    refusee:    demandes.filter(d => d.statut === "refusee").length,
  }), [demandes])

  return (
    <div className="min-h-screen bg-[#f7f9fc]">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">

        {/* En-tête */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate("/dashboard")}
              className="text-slate-400 hover:text-[#0d2a4a] text-sm font-medium"
            >
              ← Retour
            </button>
            <h1 className="text-2xl font-bold text-[#0d2a4a]">Demandes d'achat</h1>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={fetchData}
              className="flex items-center gap-2 text-sm font-semibold text-[#0d4f8a] border border-[#0d4f8a]/30 px-4 py-2 rounded-xl hover:bg-[#0d4f8a]/5 transition-colors"
            >
              <RefreshCw size={15} />
              Actualiser
            </button>
            <button
              onClick={() => navigate("/demandes/nouvelle")}
              className="flex items-center gap-2 bg-[#0d4f8a] text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-[#0a3d6b] transition-colors"
            >
              <Plus size={15} />
              Nouvelle demande
            </button>
          </div>
        </div>

        {/* Cartes stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total",      value: stats.total,      color: "text-[#0d2a4a]", bg: "bg-white" },
            { label: "En attente", value: stats.en_attente, color: "text-amber-700",  bg: "bg-amber-50" },
            { label: "Approuvées", value: stats.approuvee,  color: "text-green-700",  bg: "bg-green-50" },
            { label: "Refusées",   value: stats.refusee,    color: "text-red-700",    bg: "bg-red-50" },
          ].map(s => (
            <div key={s.label} className={`${s.bg} rounded-2xl border border-slate-200 p-4`}>
              <p className="text-xs text-slate-500 mb-1">{s.label}</p>
              <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
            </div>
          ))}
        </div>

        {/* Barre de filtres */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-3">

            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input
                type="text"
                placeholder="Objet, description, demandeur..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20 focus:border-[#0d4f8a]"
              />
            </div>

            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={15} />
              <select
                value={filter}
                onChange={e => setFilter(e.target.value)}
                className="pl-9 pr-8 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white cursor-pointer appearance-none min-w-[200px] focus:ring-2 focus:ring-[#0d4f8a]/20"
              >
                {STATUTS.map(s => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>

            {(search || filter !== "tous") && (
              <button
                onClick={resetFiltres}
                className="px-4 py-2.5 text-sm text-slate-500 hover:text-red-600 border border-slate-200 rounded-xl hover:border-red-200 transition-colors whitespace-nowrap"
              >
                ✕ Réinitialiser
              </button>
            )}
          </div>

          <p className="text-xs text-slate-400 mt-3">
            {processed.length} résultat{processed.length !== 1 ? "s" : ""} sur {demandes.length}
          </p>
        </div>

        {/* Tableau */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="animate-spin text-[#0d4f8a]" size={36} />
          </div>
        ) : processed.length === 0 ? (
          <div className="text-center py-16 text-slate-400 italic bg-white rounded-2xl border border-slate-200">
            Aucune demande ne correspond à vos critères.
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 overflow-x-auto">
            <table className="w-full text-left text-sm" style={{ tableLayout: "fixed" }}>
              <colgroup>
                <col style={{ width: "220px" }} />
                <col style={{ width: "260px" }} />
                <col style={{ width: "140px" }} />
                <col style={{ width: "110px" }} />
                <col style={{ width: "110px" }} />
                {isAdmin && <col style={{ width: "160px" }} />}
              </colgroup>
              <thead className="bg-slate-50 border-b border-slate-200 text-xs text-slate-500 uppercase tracking-wide">
                <tr>
                  <th className="px-4 py-3 font-medium">Objet</th>
                  <th className="px-4 py-3 font-medium">Description</th>
                  <th className="px-4 py-3 font-medium">Demandeur</th>
                  <th className="px-4 py-3 font-medium">Date</th>
                  <th className="px-4 py-3 font-medium">Statut</th>
                  {isAdmin && <th className="px-4 py-3 font-medium text-center">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {processed.map(d => {
                  const id = d.id_demande || d.id
                  return (
                    <tr key={id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-4 py-3 font-semibold text-[#0d2a4a] truncate">
                        {d.objet || "—"}
                      </td>
                      <td className="px-4 py-3 text-slate-500 text-xs truncate">
                        {d.description || "—"}
                      </td>
                      <td className="px-4 py-3 text-slate-600 truncate">
                        {d.demandeur_nom || "—"}
                      </td>
                      <td className="px-4 py-3 text-slate-500 text-xs">
                        {formatDate(d.date_creation)}
                      </td>
                      <td className="px-4 py-3">
                        <StatusBadge status={d.statut} />
                      </td>
                      {isAdmin && (
                        <td className="px-4 py-3">
                          {d.statut === "en_attente" && (
                            actionLoading === id ? (
                              <div className="flex justify-center">
                                <Loader2 className="animate-spin text-[#0d4f8a]" size={18} />
                              </div>
                            ) : (
                              <div className="flex justify-center gap-1.5">
                                <button
                                  onClick={() => handleAction(id, "approuve")}
                                  className="bg-green-100 text-green-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-green-200 transition-colors"
                                >
                                  Valider
                                </button>
                                <button
                                  onClick={() => handleAction(id, "refuse")}
                                  className="bg-red-100 text-red-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-red-200 transition-colors"
                                >
                                  Refuser
                                </button>
                              </div>
                            )
                          )}
                        </td>
                      )}
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  )
}