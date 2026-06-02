import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"
import { bonCommandeService } from "../../services/bonCommandeService"
import StatusBadge from "../../components/ui/StatusBadge"
import Header from "../../components/ui/Header"
import { Search, Filter, Loader2, RefreshCw } from "lucide-react"

const STATUTS = [
  { value: "tous", label: "Tous les statuts" },
  { value: "en_preparation", label: "En préparation" },
  { value: "valide_finance", label: "Validé finance" },
  { value: "expedie", label: "Expédié" },
  { value: "livre", label: "Livré" },
  { value: "annule", label: "Annulé" },
]

export default function BonCommandePage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [bcs, setBcs] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(null)

  // Filtres
  const [search, setSearch] = useState("")
  const [statutFilter, setStatutFilter] = useState("tous")
  const [fournisseurFilter, setFournisseurFilter] = useState("tous")
  const [departementFilter, setDepartementFilter] = useState("tous")

  const isFinancier = ["administrateur", "responsable_financier", "directeur"].includes(user?.role)
  const isAgent = ["administrateur", "postal_iut", "postal_univ"].includes(user?.role)

  const loadBCs = async () => {
    setLoading(true)
    try {
      const data = await bonCommandeService.getAll()
      setBcs(data || [])
    } catch (err) {
      console.error("Erreur chargement BC", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadBCs() }, [])

  // Listes dynamiques pour les selects
  const fournisseurs = useMemo(() => {
    const unique = [...new Set(bcs.map(b => b.fournisseur_nom).filter(Boolean))]
    return unique.sort()
  }, [bcs])

  const departements = useMemo(() => {
    const unique = [...new Set(bcs.map(b => b.departement_nom).filter(Boolean))]
    return unique.sort()
  }, [bcs])

  // Filtrage
  const filtered = useMemo(() => {
    return bcs.filter(bc => {
      const q = search.trim().toLowerCase()
      const matchSearch = !q ||
        bc.numero_commande?.toLowerCase().includes(q) ||
        bc.fournisseur_nom?.toLowerCase().includes(q) ||
        bc.departement_nom?.toLowerCase().includes(q) ||
        bc.createur_nom?.toLowerCase().includes(q) ||
        bc.commentaire?.toLowerCase().includes(q)

      const matchStatut = statutFilter === "tous" || bc.statut_libelle === statutFilter
      const matchFournisseur = fournisseurFilter === "tous" || bc.fournisseur_nom === fournisseurFilter
      const matchDept = departementFilter === "tous" || bc.departement_nom === departementFilter

      return matchSearch && matchStatut && matchFournisseur && matchDept
    })
  }, [bcs, search, statutFilter, fournisseurFilter, departementFilter])

  const resetFiltres = () => {
    setSearch("")
    setStatutFilter("tous")
    setFournisseurFilter("tous")
    setDepartementFilter("tous")
  }

  const handleAction = async (id, action) => {
    setActionLoading(id)
    try {
      if (action === "valider")   await bonCommandeService.valider(id)
      if (action === "expedier")  await bonCommandeService.expedier(id)
      if (action === "confirmer") await bonCommandeService.confirmerLivraison(id)
      if (action === "annuler")   await bonCommandeService.annuler(id)
      await loadBCs()
    } catch (err) {
      alert(`Erreur : ${err.message || action}`)
    } finally {
      setActionLoading(null)
    }
  }

  const formatDate = (d) => d ? new Date(d).toLocaleDateString("fr-FR") : "—"
  const formatMontant = (m) => m != null ? `${Number(m).toLocaleString("fr-FR")} €` : "—"

  // Compteurs par statut
  const stats = useMemo(() => ({
    total: bcs.length,
    en_preparation: bcs.filter(b => b.statut_libelle === "en_preparation").length,
    valide_finance: bcs.filter(b => b.statut_libelle === "valide_finance").length,
    expedie: bcs.filter(b => b.statut_libelle === "expedie").length,
  }), [bcs])

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
            <h1 className="text-2xl font-bold text-[#0d2a4a]">Bons de Commande</h1>
          </div>
          <button
            onClick={loadBCs}
            className="flex items-center gap-2 text-sm font-semibold text-[#0d4f8a] border border-[#0d4f8a]/30 px-4 py-2 rounded-xl hover:bg-[#0d4f8a]/5 transition-colors"
          >
            <RefreshCw size={15} />
            Actualiser
          </button>
        </div>

        {/* Cartes stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total", value: stats.total, color: "text-[#0d2a4a]", bg: "bg-white" },
            { label: "En préparation", value: stats.en_preparation, color: "text-blue-700", bg: "bg-blue-50" },
            { label: "Validé finance", value: stats.valide_finance, color: "text-amber-700", bg: "bg-amber-50" },
            { label: "Expédié", value: stats.expedie, color: "text-orange-700", bg: "bg-orange-50" },
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

            {/* Recherche */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input
                type="text"
                placeholder="Numéro, fournisseur, département, créateur..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20 focus:border-[#0d4f8a]"
              />
            </div>

            {/* Filtre statut */}
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={15} />
              <select
                value={statutFilter}
                onChange={e => setStatutFilter(e.target.value)}
                className="pl-9 pr-8 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white cursor-pointer appearance-none min-w-[180px] focus:ring-2 focus:ring-[#0d4f8a]/20"
              >
                {STATUTS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
              </select>
            </div>

            {/* Filtre fournisseur */}
            {fournisseurs.length > 0 && (
              <select
                value={fournisseurFilter}
                onChange={e => setFournisseurFilter(e.target.value)}
                className="px-4 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white cursor-pointer appearance-none min-w-[160px] focus:ring-2 focus:ring-[#0d4f8a]/20"
              >
                <option value="tous">Tous fournisseurs</option>
                {fournisseurs.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
            )}

            {/* Filtre département */}
            {departements.length > 0 && (
              <select
                value={departementFilter}
                onChange={e => setDepartementFilter(e.target.value)}
                className="px-4 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white cursor-pointer appearance-none min-w-[160px] focus:ring-2 focus:ring-[#0d4f8a]/20"
              >
                <option value="tous">Tous départements</option>
                {departements.map(d => <option key={d} value={d}>{d}</option>)}
              </select>
            )}

            {/* Reset */}
            {(search || statutFilter !== "tous" || fournisseurFilter !== "tous" || departementFilter !== "tous") && (
              <button
                onClick={resetFiltres}
                className="px-4 py-2.5 text-sm text-slate-500 hover:text-red-600 border border-slate-200 rounded-xl hover:border-red-200 transition-colors whitespace-nowrap"
              >
                ✕ Réinitialiser
              </button>
            )}
          </div>

          {/* Résultats */}
          <p className="text-xs text-slate-400 mt-3">
            {filtered.length} résultat{filtered.length !== 1 ? "s" : ""} sur {bcs.length}
          </p>
        </div>

        {/* Tableau */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="animate-spin text-[#0d4f8a]" size={36} />
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 text-slate-400 italic bg-white rounded-2xl border border-slate-200">
            Aucun bon de commande ne correspond à vos critères.
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 overflow-x-auto">
            <table className="w-full text-left text-sm" style={{ tableLayout: "fixed" }}>
              <colgroup>
                <col style={{ width: "140px" }} />
                <col style={{ width: "140px" }} />
                <col style={{ width: "150px" }} />
                <col style={{ width: "120px" }} />
                <col style={{ width: "110px" }} />
                <col style={{ width: "110px" }} />
                <col style={{ width: "110px" }} />
                <col style={{ width: "180px" }} />
              </colgroup>
              <thead className="bg-slate-50 border-b border-slate-200 text-xs text-slate-500 uppercase tracking-wide">
                <tr>
                  <th className="px-4 py-3 font-medium">N° commande</th>
                  <th className="px-4 py-3 font-medium">Département</th>
                  <th className="px-4 py-3 font-medium">Fournisseur</th>
                  <th className="px-4 py-3 font-medium">Montant</th>
                  <th className="px-4 py-3 font-medium">Date cmd</th>
                  <th className="px-4 py-3 font-medium">Livraison est.</th>
                  <th className="px-4 py-3 font-medium">Statut</th>
                  <th className="px-4 py-3 font-medium text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filtered.map(bc => (
                  <tr key={bc.id_bon_commande} className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-3 font-mono text-xs font-semibold text-[#0d2a4a] truncate">
                      {bc.numero_commande || "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-700 truncate">
                      {bc.departement_nom || "—"}
                    </td>
                    <td className="px-4 py-3 text-slate-700 truncate">
                      {bc.fournisseur_nom || "—"}
                    </td>
                    <td className="px-4 py-3 font-semibold text-[#0d2a4a]">
                      {formatMontant(bc.montant_estime)}
                    </td>
                    <td className="px-4 py-3 text-slate-500 text-xs">
                      {formatDate(bc.date_commande)}
                    </td>
                    <td className="px-4 py-3 text-slate-500 text-xs">
                      {formatDate(bc.date_estimee_livraison)}
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge status={bc.statut_libelle} />
                    </td>
                    <td className="px-4 py-3">
                      {actionLoading === bc.id_bon_commande ? (
                        <div className="flex justify-center">
                          <Loader2 className="animate-spin text-[#0d4f8a]" size={18} />
                        </div>
                      ) : (
                        <div className="flex justify-center gap-1.5 flex-wrap">
                          {bc.statut_libelle === "en_preparation" && isFinancier && (
                            <button
                              onClick={() => handleAction(bc.id_bon_commande, "valider")}
                              className="bg-blue-100 text-blue-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-blue-200 transition-colors"
                            >
                              Valider
                            </button>
                          )}
                          {bc.statut_libelle === "valide_finance" && isFinancier && (
                            <button
                              onClick={() => handleAction(bc.id_bon_commande, "expedier")}
                              className="bg-orange-100 text-orange-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-orange-200 transition-colors"
                            >
                              Expédier
                            </button>
                          )}
                          {bc.statut_libelle === "expedie" && isAgent && (
                            <button
                              onClick={() => handleAction(bc.id_bon_commande, "confirmer")}
                              className="bg-green-100 text-green-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-green-200 transition-colors"
                            >
                              Livré
                            </button>
                          )}
                          {["en_preparation", "valide_finance"].includes(bc.statut_libelle) && isFinancier && (
                            <button
                              onClick={() => handleAction(bc.id_bon_commande, "annuler")}
                              className="bg-red-100 text-red-700 px-2.5 py-1 rounded-lg text-xs font-medium hover:bg-red-200 transition-colors"
                            >
                              Annuler
                            </button>
                          )}
                        </div>
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