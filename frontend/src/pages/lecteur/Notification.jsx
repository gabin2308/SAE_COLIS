import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { notificationService } from "../../services/notificationService"
import Header from "../../components/ui/Header"
import { Bell, Check, Trash2, Loader2, Filter, RefreshCw, Search } from "lucide-react"

export default function NotificationsPage() {
  const navigate = useNavigate()
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState("toutes")

  const fetchData = async () => {
    setLoading(true)
    try {
      const data = await notificationService.getMesNotifications()
      setNotifications(data || [])
    } catch (err) {
      console.error("Erreur chargement notifications", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [])

  const processedNotifications = useMemo(() => {
    return notifications.filter(n => {
      if (filter === "lues") return n.lue === 1 || n.lue === true
      if (filter === "non-lues") return n.lue === 0 || n.lue === false
      return true
    })
  }, [notifications, filter])

  const stats = useMemo(() => ({
    total: notifications.length,
    nonLues: notifications.filter(n => !n.lue).length
  }), [notifications])

  const handleAction = async (action, id = null) => {
    try {
      if (action === "lu") await notificationService.marquerLu(id)
      else if (action === "toutLu") await notificationService.marquerToutesLues()
      else if (action === "delete") await notificationService.delete(id)
      fetchData()
    } catch (err) {
      alert("Une erreur est survenue.")
    }
  }

  return (
    <div className="min-h-screen bg-[#f7f9fc]">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        
        {/* En-tête */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button onClick={() => navigate("/dashboard")} className="text-slate-400 hover:text-[#0d2a4a] text-sm font-medium">← Retour</button>
            <h1 className="text-2xl font-bold text-[#0d2a4a]">Notifications</h1>
          </div>
          <button onClick={fetchData} className="flex items-center gap-2 text-sm font-semibold text-[#0d4f8a] border border-[#0d4f8a]/30 px-4 py-2 rounded-xl hover:bg-[#0d4f8a]/5">
            <RefreshCw size={15} /> Actualiser
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div className="bg-white rounded-2xl border border-slate-200 p-4">
            <p className="text-xs text-slate-500 mb-1">Total</p>
            <p className="text-2xl font-bold text-[#0d2a4a]">{stats.total}</p>
          </div>
          <div className="bg-blue-50 rounded-2xl border border-blue-100 p-4">
            <p className="text-xs text-blue-600 mb-1">Non lues</p>
            <p className="text-2xl font-bold text-blue-700">{stats.nonLues}</p>
          </div>
        </div>

        {/* Barre de contrôle unifiée (Filtre + Action) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 mb-6 flex items-center justify-between gap-4">
          <div className="relative flex-1">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <select 
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="w-full pl-9 pr-8 py-2.5 text-sm border border-slate-200 rounded-xl outline-none bg-white cursor-pointer focus:ring-2 focus:ring-[#0d4f8a]/20"
            >
              <option value="toutes">Afficher : Toutes les notifications</option>
              <option value="non-lues">Afficher : Non-lues uniquement</option>
              <option value="lu">Afficher : Déjà lues</option>
            </select>
          </div>
          {stats.nonLues > 0 && (
            <button onClick={() => handleAction("toutLu")} className="text-sm text-blue-600 font-semibold hover:bg-blue-50 px-4 py-2.5 rounded-xl transition-colors whitespace-nowrap">
              Tout marquer lu
            </button>
          )}
        </div>

        {/* Liste */}
        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="animate-spin text-[#0d4f8a]" size={36} /></div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            {processedNotifications.length > 0 ? (
              <ul className="divide-y divide-slate-100">
                {processedNotifications.map((n) => (
                  <li key={n.id_notification} className={`p-4 flex items-center justify-between hover:bg-slate-50 transition-colors ${!n.lue ? 'bg-blue-50/20' : ''}`}>
                    <div className="flex items-center gap-4">
                      <div className={`p-2 rounded-full ${!n.lue ? 'bg-blue-100 text-blue-600' : 'bg-slate-100 text-slate-400'}`}>
                        <Bell size={18} />
                      </div>
                      <div>
                        <p className={`text-sm ${!n.lue ? 'font-bold text-[#0d2a4a]' : 'text-slate-600'}`}>{n.message}</p>
                        <p className="text-xs text-slate-400">{new Date(n.date_creation).toLocaleString()}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {!n.lue && (
                        <button onClick={() => handleAction("lu", n.id_notification)} className="p-2 text-slate-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                          <Check size={18} />
                        </button>
                      )}
                      <button onClick={() => handleAction("delete", n.id_notification)} className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="p-12 text-center text-slate-400 italic">Aucune notification trouvée.</div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}