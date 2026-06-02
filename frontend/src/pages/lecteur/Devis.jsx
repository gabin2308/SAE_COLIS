import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { devisService } from "../../services/devisService"
import { useAuth } from "../../context/AuthContext"
import StatusBadge from "../../components/ui/StatusBadge"
import Header from "../../components/ui/Header"
import { Search, Filter, Loader2, RefreshCw, Download, Check, X } from "lucide-react"

const STATUTS_DEVIS = [
  { value: "tous", label: "Tous les statuts" },
  { value: "en_attente", label: "En attente" },
  { value: "accepte", label: "Accepté" },
  { value: "refuse", label: "Refusé" },
]

export default function DevisPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [devisList, setDevisList] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(null)
  const [downloadingId, setDownloadingId] = useState(null)

  const [search, setSearch] = useState("")
  const [statusFilter, setStatusFilter] = useState("tous")

  const fetchData = async () => {
    setLoading(true)
    try {
      const data = await devisService.getAll()
      setDevisList(data || [])
    } catch (err) {
      console.error("Erreur chargement devis", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [])

  const filteredDevis = useMemo(() => {
    return devisList.filter(d => {
      const q = search.trim().toLowerCase()
      const matchSearch = !q ||
        d.objet?.toLowerCase().includes(q) ||
        d.fournisseur_nom?.toLowerCase().includes(q) ||
        d.createur_nom?.toLowerCase().includes(q)
      const matchStatus = statusFilter === "tous" || d.statut === statusFilter
      return matchSearch && matchStatus
    })
  }, [devisList, search, statusFilter])

  const stats = useMemo(() => ({
    total: devisList.length,
    attente: devisList.filter(d => d.statut === "en_attente").length,
    accepte: devisList.filter(d => d.statut === "accepte").length,
    refuse: devisList.filter(d => d.statut === "refuse").length,
  }), [devisList])

  const handleAction = async (id, action) => {
    setActionLoading(id)
    try {
      action === "accepter" ? await devisService.accepter(id) : await devisService.refuser(id)
      await fetchData()
    } catch (err) {
      alert("Erreur lors de l'action.")
    } finally {
      setActionLoading(null)
    }
  }

  const handleDownload = async (id) => {
    setDownloadingId(id)
    try {
      await devisService.telechargerPdf(id)
    } catch (err) {
      alert("Impossible de télécharger le PDF.")
    } finally {
      setDownloadingId(null)
    }
  }

  return (
    <div className="min-h-screen bg-[#f7f9fc]">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">

        {/* En-tête */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button onClick={() => navigate("/dashboard")} className="text-slate-400 hover:text-[#0d2a4a] text-sm font-medium">← Retour</button>
            <h1 className="text-2xl font-bold text-[#0d2a4a]">Suivi des Devis</h1>
          </div>
          <button onClick={fetchData} className="flex items-center gap-2 text-sm font-semibold text-[#0d4f8a] border border-[#0d4f8a]/30 px-4 py-2 rounded-xl hover:bg-[#0d4f8a]/5 transition-colors">
            <RefreshCw size={15} /> Actualiser
          </button>
        </div>

        {/* Cartes stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total", value: stats.total, color: "text-[#0d2a4a]", bg: "bg-white" },
            { label: "En attente", value: stats.attente, color: "text-amber-700", bg: "bg-amber-50" },
            { label: "Acceptés", value: stats.accepte, color: "text-green-700", bg: "bg-green-50" },
            { label: "Refusés", value: stats.refuse, color: "text-red-700", bg: "bg-red-50" },
          ].map(s => (
            <div key={s.label} className={`${s.bg} rounded-2xl border border-slate-200 p-4`}>
              <p className="text-xs text-slate-500 mb-1">{s.label}</p>
              <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
            </div>
          ))}
        </div>

        {/* Filtres */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 mb-6 flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input 
              type="text" 
              placeholder="Rechercher par objet, fournisseur, créateur..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20"
            />
          </div>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={15} />
            <select 
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="pl-9 pr-8 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white min-w-[200px] cursor-pointer"
            >
              {STATUTS_DEVIS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
        </div>

        {/* Tableau */}
        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="animate-spin text-[#0d4f8a]" size={36} /></div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 border-b border-slate-200 text-xs text-slate-500 uppercase tracking-wide">
                <tr>
                  <th className="px-4 py-3">Objet</th>
                  <th className="px-4 py-3">Fournisseur</th>
                  <th className="px-4 py-3">Montant</th>
                  <th className="px-4 py-3">Statut</th>
                  <th className="px-4 py-3 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredDevis.map(d => (
                  <tr key={d.id_devis} className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-3 font-medium text-[#0d2a4a]">{d.objet}</td>
                    <td className="px-4 py-3 text-slate-600">{d.fournisseur_nom || "—"}</td>
                    <td className="px-4 py-3 font-semibold">{d.montant_estime} €</td>
                    <td className="px-4 py-3"><StatusBadge status={d.statut} /></td>
                    <td className="px-4 py-3 flex justify-center gap-2">
                      {d.fichier_pdf && (
                        <button onClick={() => handleDownload(d.id_devis)} className="p-1.5 text-slate-400 hover:text-blue-600 rounded-lg hover:bg-blue-50">
                          {downloadingId === d.id_devis ? <Loader2 className="animate-spin" size={16}/> : <Download size={16} />}
                        </button>
                      )}
                      {d.statut === 'en_attente' && (
                        actionLoading === d.id_devis ? <Loader2 className="animate-spin" size={16}/> : (
                          <>
                            <button onClick={() => handleAction(d.id_devis, "accepter")} className="p-1.5 bg-green-50 text-green-600 rounded-lg hover:bg-green-100"><Check size={16}/></button>
                            <button onClick={() => handleAction(d.id_devis, "refuser")} className="p-1.5 bg-red-50 text-red-600 rounded-lg hover:bg-red-100"><X size={16}/></button>
                          </>
                        )
                      )}
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