import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

const API = "/api"

async function fetchJson(url) {
  try {
    const res = await fetch(url, { credentials: "include" })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

function StatCard({ label, value, icon, color }) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-5 flex items-center gap-4 shadow-sm">
      <div className={`w-12 h-12 rounded-lg flex items-center justify-center text-2xl ${color}`}>
        {icon}
      </div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-900">
          {value === null ? <span className="text-gray-300 text-base">—</span> : value}
        </p>
      </div>
    </div>
  )
}

function Badge({ statut }) {
  const map = {
    en_attente:     "bg-yellow-100 text-yellow-700",
    approuvee:      "bg-green-100 text-green-700",
    refusee:        "bg-red-100 text-red-700",
    en_preparation: "bg-blue-100 text-blue-700",
    envoye:         "bg-indigo-100 text-indigo-700",
    en_transit:     "bg-purple-100 text-purple-700",
    livre:          "bg-green-100 text-green-700",
    annule:         "bg-gray-100 text-gray-500",
    accepte:        "bg-green-100 text-green-700",
    refuse:         "bg-red-100 text-red-700",
  }
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${map[statut] ?? "bg-gray-100 text-gray-500"}`}>
      {statut?.replace(/_/g, " ")}
    </span>
  )
}

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats]       = useState({})
  const [colis, setColis]       = useState([])
  const [demandes, setDemandes] = useState([])
  const [bons, setBons]         = useState([])
  const [notifs, setNotifs]     = useState([])
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    async function load() {
      const [
        allColis, allDemandes, allBons,
        allUsers, allDeps, allFournis,
        mesNotifs, notifsCount
      ] = await Promise.all([
        fetchJson(`${API}/colis/`),
        fetchJson(`${API}/demande_achat/`),
        fetchJson(`${API}/bon_commande/`),
        fetchJson(`${API}/users/`),
        fetchJson(`${API}/departement/`),
        fetchJson(`${API}/fournisseur/`),
        fetchJson(`${API}/notification/`),
        fetchJson(`${API}/notification/count`),
      ])

      setStats({
        colis:    Array.isArray(allColis)    ? allColis.length    : null,
        demandes: Array.isArray(allDemandes) ? allDemandes.length : null,
        bons:     Array.isArray(allBons)     ? allBons.length     : null,
        users:    Array.isArray(allUsers)    ? allUsers.length    : null,
        deps:     Array.isArray(allDeps)     ? allDeps.length     : null,
        fournis:  Array.isArray(allFournis)  ? allFournis.length  : null,
        nonLues:  notifsCount?.count ?? null,
      })

      setColis(Array.isArray(allColis) ? allColis.slice(0, 5) : [])
      setDemandes(Array.isArray(allDemandes) ? allDemandes.filter(d => d.statut === "en_attente").slice(0, 5) : [])
      setBons(Array.isArray(allBons) ? allBons.slice(0, 5) : [])
      setNotifs(Array.isArray(mesNotifs) ? mesNotifs.filter(n => !n.lu).slice(0, 5) : [])
      setLoading(false)
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400 text-sm">
        Chargement du dashboard…
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Tableau de bord</h1>
        <p className="text-sm text-gray-500 mt-1">Vue d'ensemble de l'activité</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <StatCard label="Colis total"      value={stats.colis}    icon="📦" color="bg-indigo-50" />
        <StatCard label="Demandes d'achat" value={stats.demandes}  icon="📝" color="bg-yellow-50" />
        <StatCard label="Bons de commande" value={stats.bons}      icon="📋" color="bg-blue-50" />
        <StatCard label="Utilisateurs"     value={stats.users}     icon="👥" color="bg-green-50" />
        <StatCard label="Départements"     value={stats.deps}      icon="🏢" color="bg-purple-50" />
        <StatCard label="Fournisseurs"     value={stats.fournis}   icon="🏭" color="bg-orange-50" />
        <StatCard label="Notifs non lues"  value={stats.nonLues}   icon="🔔" color="bg-red-50" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-800">Derniers colis</h2>
            <Link to="/admin/colis" className="text-xs text-indigo-600 hover:underline">Voir tout →</Link>
          </div>
          {colis.length === 0 ? (
            <p className="text-sm text-gray-400">Aucun colis</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-gray-400 border-b border-gray-100">
                  <th className="pb-2 font-medium">N° suivi</th>
                  <th className="pb-2 font-medium">Destinataire</th>
                  <th className="pb-2 font-medium">Statut</th>
                </tr>
              </thead>
              <tbody>
                {colis.map(c => (
                  <tr key={c.id_colis} className="border-b border-gray-50 last:border-0">
                    <td className="py-2 text-gray-600 font-mono text-xs">{c.numero_suivi ?? "—"}</td>
                    <td className="py-2 text-gray-700">{c.destinataire_nom ?? "—"}</td>
                    <td className="py-2"><Badge statut={c.statut_libelle} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-800">Demandes en attente</h2>
            <Link to="/admin/demande_achat" className="text-xs text-indigo-600 hover:underline">Voir tout →</Link>
          </div>
          {demandes.length === 0 ? (
            <p className="text-sm text-gray-400">Aucune demande en attente</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-gray-400 border-b border-gray-100">
                  <th className="pb-2 font-medium">Objet</th>
                  <th className="pb-2 font-medium">Demandeur</th>
                  <th className="pb-2 font-medium">Montant</th>
                </tr>
              </thead>
              <tbody>
                {demandes.map(d => (
                  <tr key={d.id_demande} className="border-b border-gray-50 last:border-0">
                    <td className="py-2 text-gray-700 truncate max-w-[140px]">{d.objet}</td>
                    <td className="py-2 text-gray-600">{d.demandeur_nom ?? "—"}</td>
                    <td className="py-2 text-gray-600">
                      {d.montant_estime ? `${d.montant_estime} €` : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-800">Derniers bons de commande</h2>
            <Link to="/admin/bon_commande" className="text-xs text-indigo-600 hover:underline">Voir tout →</Link>
          </div>
          {bons.length === 0 ? (
            <p className="text-sm text-gray-400">Aucun bon de commande</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-gray-400 border-b border-gray-100">
                  <th className="pb-2 font-medium">Numéro</th>
                  <th className="pb-2 font-medium">Département</th>
                  <th className="pb-2 font-medium">Statut</th>
                </tr>
              </thead>
              <tbody>
                {bons.map(b => (
                  <tr key={b.id_bon_commande} className="border-b border-gray-50 last:border-0">
                    <td className="py-2 font-mono text-xs text-gray-600">{b.numero_commande}</td>
                    <td className="py-2 text-gray-700">{b.departement_nom ?? "—"}</td>
                    <td className="py-2"><Badge statut={b.statut} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-800">Notifications non lues</h2>
            <Link to="/admin/notification" className="text-xs text-indigo-600 hover:underline">Voir tout →</Link>
          </div>
          {notifs.length === 0 ? (
            <p className="text-sm text-gray-400">Aucune notification non lue</p>
          ) : (
            <ul className="space-y-2">
              {notifs.map(n => (
                <li key={n.id_notification} className="flex items-start gap-3 p-3 bg-indigo-50 rounded-lg">
                  <span className="text-indigo-400 mt-0.5 shrink-0">🔔</span>
                  <div>
                    <p className="text-sm text-gray-700">{n.message_notification}</p>
                    <p className="text-xs text-gray-400 mt-0.5">{n.date_envoi}</p>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

      </div>
    </div>
  )
}