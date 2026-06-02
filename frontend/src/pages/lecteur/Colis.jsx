import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { colisService } from "../../services/colisService"
import { useAuth } from "../../context/AuthContext"
import StatusBadge from "../../components/ui/StatusBadge"
import Header from "../../components/ui/Header"
import { Search, Filter, Loader2, RefreshCw } from "lucide-react"

const STATUTS_COLIS = [
  { value: "tous", label: "Tous les statuts" },
  { value: "recu_universite", label: "Reçu université" },
  { value: "transfere_iut", label: "Transféré IUT" },
  { value: "en_attente_retrait", label: "En attente retrait" },
  { value: "remis_destinataire", label: "Remis destinataire" },
  { value: "incident", label: "Incident" },
]

export default function Colis() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [colisList, setColisList] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(null)

  const [search, setSearch] = useState("")
  const [statusFilter, setStatusFilter] = useState("tous")

  const isAgent = ["administrateur", "postal_iut", "postal_univ"].includes(user?.role)

  const fetchData = async () => {
    setLoading(true)
    try {
      const data = isAgent
        ? await colisService.getAll()
        : await colisService.getMesColis()
      setColisList(data || [])
    } catch (err) {
      console.error("Erreur chargement colis", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [user])

  const filteredColis = useMemo(() => {
    return colisList.filter(c => {
      const q = search.trim().toLowerCase()
      const matchSearch = !q ||
        c.numero_suivi?.toLowerCase().includes(q) ||
        c.numero_commande?.toLowerCase().includes(q) ||
        c.destinataire_nom?.toLowerCase().includes(q) ||
        c.receptionne_par_nom?.toLowerCase().includes(q) ||
        c.commentaire?.toLowerCase().includes(q)
      const matchStatus = statusFilter === "tous" || c.statut_libelle === statusFilter
      return matchSearch && matchStatus
    })
  }, [colisList, search, statusFilter])

  const resetFiltres = () => {
    setSearch("")
    setStatusFilter("tous")
  }

  const handleColisAction = async (id, action) => {
    setActionLoading(id)
    try {
      if (action === "receptionner") await colisService.receptionner(id)
      else if (action === "transferer") await colisService.transfererIut(id)
      else if (action === "retirer")   await colisService.retirer(id)
      else if (action === "signaler")  await colisService.signalerIncident(id)
      await fetchData()
    } catch (err) {
      console.error("Erreur action colis:", err)
    } finally {
      setActionLoading(null)
    }
  }

  const formatDate = (d) => d ? new Date(d).toLocaleDateString("fr-FR") : "—"

  const stats = useMemo(() => ({
    total:   colisList.length,
    recu:    colisList.filter(c => c.statut_libelle === "recu_universite").length,
    attente: colisList.filter(c => c.statut_libelle === "en_attente_retrait").length,
    incident:colisList.filter(c => c.statut_libelle === "incident").length,
  }), [colisList])

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
            <h1 className="text-2xl font-bold text-[#0d2a4a]">Gestion des Colis</h1>
          </div>
          <button
            onClick={fetchData}
            className="flex items-center gap-2 text-sm font-semibold text-[#0d4f8a] border border-[#0d4f8a]/30 px-4 py-2 rounded-xl hover:bg-[#0d4f8a]/5 transition-colors"
          >
            <RefreshCw size={15} />
            Actualiser
          </button>
        </div>

        {/* Cartes stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total",              value: stats.total,    color: "text-[#0d2a4a]", bg: "bg-white" },
            { label: "Reçus université",   value: stats.recu,     color: "text-blue-700",  bg: "bg-blue-50" },
            { label: "En attente retrait", value: stats.attente,  color: "text-amber-700", bg: "bg-amber-50" },
            { label: "Incidents",          value: stats.incident, color: "text-red-700",   bg: "bg-red-50" },
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
                placeholder="N° suivi, N° commande, destinataire, réceptionné par..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20 focus:border-[#0d4f8a]"
              />
            </div>

            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={15} />
              <select
                value={statusFilter}
                onChange={e => setStatusFilter(e.target.value)}
                className="pl-9 pr-8 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white cursor-pointer appearance-none min-w-[200px] focus:ring-2 focus:ring-[#0d4f8a]/20"
              >
                {STATUTS_COLIS.map(s => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>

            {(search || statusFilter !== "tous") && (
              <button
                onClick={resetFiltres}
                className="px-4 py-2.5 text-sm text-slate-500 hover:text-red-600 border border-slate-200 rounded-xl hover:border-red-200 transition-colors whitespace-nowrap"
              >
                ✕ Réinitialiser
              </button>
            )}
          </div>

          <p className="text-xs text-slate-400 mt-3">
            {filteredColis.length} résultat{filteredColis.length !== 1 ? "s" : ""} sur {colisList.length}
          </p>
        </div>

        {/* Tableau */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="animate-spin text-[#0d4f8a]" size={36} />
          </div>
        ) : filteredColis.length === 0 ? (
          <div className="text-center py-16 text-slate-400 italic bg-white rounded-2xl border border-slate-200">
            Aucun colis ne correspond à vos critères.
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 overflow-x-auto">
            <table className="w-full text-left text-sm" style={{ tableLayout: "fixed" }}>
              <colgroup>
                <col style={{ width: "155px" }} />
                <col style={{ width: "140px" }} />
                <col style={{ width: "150px" }} />
                <col style={{ width: "150px" }} />
                <col style={{ width: "100px" }} />
                <col style={{ width: "100px" }} />
                <col style={{ width: "130px" }} />
                {isAgent && <col style={{ width: "220px" }} />}
              </colgroup>
              <thead className="bg-slate-50 border-b border-slate-200 text-xs text-slate-500 uppercase tracking-wide">
                <tr>
                  <th className="px-4 py-3 font-medium">N° suivi</th>
                  <th className="px-4 py-3 font-medium">N° commande</th>
                  <th className="px-4 py-3 font-medium">Destinataire</th>
                  <th className="px-4 py-3 font-medium">Réceptionné par</th>
                  <th className="px-4 py-3 font-medium">Réception</th>
                  <th className="px-4 py-3 font-medium">Retrait</th>
                  <th className="px-4 py-3 font-medium">Statut</th>
                  {isAgent && <th className="px-4 py-3 font-medium text-center">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredColis.map(c => (
                  <tr key={c.id_colis} className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-3 font-mono text-xs font-semibold text-[#0d2a4a] truncate">
                      {c.numero_suivi || "—"}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-slate-500 truncate">
                      {c.numero_commande || "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-700 truncate">
                      {c.destinataire_nom || "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-600 text-xs truncate">
                      {c.receptionne_par_nom || "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-500 text-xs">
                      {formatDate(c.date_reception)}
                    </td>
                    <td className="px-4 py-3 text-slate-500 text-xs">
                      {formatDate(c.date_retrait)}
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge status={c.statut_libelle} />
                    </td>
                    {isAgent && (
                      <td className="px-4 py-3">
                        {actionLoading === c.id_colis ? (
                          <div className="flex justify-center">
                            <Loader2 className="animate-spin text-[#0d4f8a]" size={18} />
                          </div>
                        ) : (
                          <div className="flex justify-center gap-1.5 flex-wrap">
                            {c.statut_libelle === "recu_universite" && (
                              <button
                                onClick={() => handleColisAction(c.id_colis, "receptionner")}
                                className="bg-blue-100 text-blue-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-blue-200 transition-colors"
                              >
                                Réceptionner
                              </button>
                            )}
                            {c.statut_libelle === "en_attente_retrait" && (
                              <button
                                onClick={() => handleColisAction(c.id_colis, "retirer")}
                                className="bg-green-100 text-green-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-green-200 transition-colors"
                              >
                                Retirer
                              </button>
                            )}
                            {c.statut_libelle !== "remis_destinataire" && (
                              <button
                                onClick={() => handleColisAction(c.id_colis, "transferer")}
                                className="bg-orange-100 text-orange-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-orange-200 transition-colors"
                              >
                                Transférer
                              </button>
                            )}
                            {c.statut_libelle !== "incident" && c.statut_libelle !== "remis_destinataire" && (
                              <button
                                onClick={() => handleColisAction(c.id_colis, "signaler")}
                                className="bg-red-100 text-red-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-red-200 transition-colors"
                              >
                                Incident
                              </button>
                            )}
                          </div>
                        )}
                      </td>
                    )}
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