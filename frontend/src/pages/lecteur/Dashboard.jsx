import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"
import { colisService } from "../../services/colisService"
import { demandeService } from "../../services/demandeService"
import { devisService } from "../../services/devisService"
import { notificationService } from "../../services/notificationService"
import { bonCommandeService } from "../../services/bonCommandeService"
import { userService } from "../../services/UtilisateurService"
import Header from "../../components/ui/Header"
import WelcomeRow from "../../components/ui/WelcomeRow"
import StatusBadge from "../../components/ui/StatusBadge"
import { DashCard, Empty } from "../../components/ui/DashCard"
import { Search, RefreshCw, Loader2, Bell, Package, FileText, ShoppingCart, Receipt, Users } from "lucide-react"

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [allColis, setAllColis] = useState([])
  const [demandes, setDemandes] = useState([])
  const [devis, setDevis] = useState([])
  const [notifications, setNotifications] = useState([])
  const [bonCommandes, setBonCommandes] = useState([])
  const [users, setUsers] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)

  const isAgent = ["administrateur", "postal_iut", "postal_univ"].includes(user?.role)
  const isFinancier = ["administrateur", "responsable_financier", "directeur"].includes(user?.role)
  const isAdmin = user?.role === "administrateur"

  const loadData = async () => {
    setLoading(true)
    try {
      const [colisData, demandesData, devisData, notifsData, bcData, usersData] = await Promise.all([
        isAgent ? colisService.getAll() : colisService.getMesColis(),
        isAdmin ? demandeService.getAll() : demandeService.getMesDemandes(),
        isFinancier ? devisService.getAll() : Promise.resolve([]),
        notificationService.getNonLues(),
        bonCommandeService.getAll(),
        isAdmin ? userService.getAll() : Promise.resolve([])
      ])
      setAllColis(colisData || [])
      setDemandes(demandesData || [])
      setDevis(devisData || [])
      setNotifications(notifsData || [])
      setBonCommandes(bcData || [])
      setUsers(usersData || [])
    } catch (err) {
      console.error("Erreur chargement dashboard", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { if (user) loadData() }, [user])

  const filteredColis = useMemo(() => {
    const q = searchTerm.trim().toLowerCase()
    if (!q) return allColis
    return allColis.filter(c =>
      c.numero_suivi?.toLowerCase().includes(q) ||
      c.numero_commande?.toLowerCase().includes(q) ||
      c.destinataire_nom?.toLowerCase().includes(q)
    )
  }, [allColis, searchTerm])

  const stats = useMemo(() => [
    { label: "Colis", value: allColis.length, color: "text-blue-700", bg: "bg-blue-50", path: "/colis" },
    { label: "Demandes", value: demandes.length, color: "text-violet-700", bg: "bg-violet-50", path: "/demandes" },
    { label: "Bons commande", value: bonCommandes.length, color: "text-amber-700", bg: "bg-amber-50", path: "/bon-commande" },
    ...(isFinancier ? [{ label: "Devis", value: devis.length, color: "text-teal-700", bg: "bg-teal-50", path: "/devis" }] : []),
  ], [allColis, demandes, bonCommandes, devis, isFinancier])

  return (
    <div className="min-h-screen bg-[#f7f9fc]">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <WelcomeRow
            prenom={user?.prenom}
            onScanClick={() => navigate("/scan")}
            onNewDemandeClick={() => navigate("/demandes/nouvelle")}
          />
        </div>

        <div className="flex gap-3 items-center bg-white px-4 py-3 rounded-2xl border border-slate-200 mb-8">
          <Search size={16} className="text-slate-400 shrink-0" />
          <input
            type="text"
            placeholder="Rechercher par numéro de suivi, commande, destinataire..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="flex-1 text-sm outline-none text-slate-700 placeholder:text-slate-400"
          />
          <button
            onClick={loadData}
            className="flex items-center gap-2 bg-[#0d4f8a] text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-[#0a3d6b] transition-colors shrink-0"
          >
            <RefreshCw size={14} />
            Actualiser
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center py-24">
            <Loader2 className="animate-spin text-[#0d4f8a]" size={36} />
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
            {stats.map(s => (
              <button key={s.label} onClick={() => navigate(s.path)} className={`${s.bg} rounded-2xl border border-slate-200 p-4 text-left hover:shadow-sm transition-shadow`}>
                <p className="text-xs text-slate-500 mb-1">{s.label}</p>
                <p className={`text-3xl font-bold ${s.color}`}>{s.value}</p>
              </button>
            ))}
          </div>
        )}

        {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Notifications */}
          <DashCard icon={<Bell size={16} />} title="Notifications" count={notifications.length} onAction={() => navigate("/notifications")} accentClass="text-blue-600 bg-blue-50">
            {notifications.length === 0 ? <Empty text="Aucune nouvelle notification." /> : <div className="p-3 bg-blue-50/60 rounded-xl border border-blue-100 text-sm"><p className="text-[#0d2a4a] font-medium truncate">{notifications[0].message}</p></div>}
          </DashCard>

          {/* Colis */}
          <DashCard icon={<Package size={16} />} title="Colis récents" count={filteredColis.length} onAction={() => navigate("/colis")} accentClass="text-indigo-600 bg-indigo-50">
            {filteredColis.length === 0 ? <Empty text="Aucun colis." /> : <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100"><p className="font-bold text-[#0d2a4a] text-sm truncate">{filteredColis[0].numero_suivi}</p><StatusBadge status={filteredColis[0].statut_libelle} /></div>}
          </DashCard>

          {/* Demandes */}
          <DashCard icon={<FileText size={16} />} title="Demandes d'achat" count={demandes.length} onAction={() => navigate("/demandes")} accentClass="text-violet-600 bg-violet-50">
            {demandes.length === 0 ? <Empty text="Aucune demande." /> : <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100"><p className="text-sm font-semibold truncate text-[#0d2a4a]">{demandes[0].objet}</p></div>}
          </DashCard>

          {/* Bons de commande */}
          <DashCard icon={<ShoppingCart size={16} />} title="Bons de commande" count={bonCommandes.length} onAction={() => navigate("/bon-commande")} accentClass="text-amber-600 bg-amber-50">
            {bonCommandes.length === 0 ? <Empty text="Aucun bon de commande." /> : <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100"><p className="font-bold text-[#0d2a4a] text-sm truncate">{bonCommandes[0].numero_commande}</p><StatusBadge status={bonCommandes[0].statut_libelle} /></div>}
          </DashCard>

          {/* Utilisateurs (Admin uniquement) */}
          {isAdmin && (
            <DashCard icon={<Users size={16} />} title="Utilisateurs" count={users.length} onAction={() => navigate("/utilisateurs")} accentClass="text-emerald-600 bg-emerald-50">
              {users.length === 0 ? <Empty text="Aucun utilisateur." /> : <div className="p-3 bg-slate-50 rounded-xl border border-slate-100"><p className="font-bold text-[#0d2a4a] text-sm">{users[0].full_name}</p></div>}
            </DashCard>
          )}
        </div>
      )}
      </main>
    </div>
  )
}