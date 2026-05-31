// import { useEffect, useState } from "react"
// import { Link } from "react-router-dom"
// import { useAuth } from "../../context/AuthContext"
// import StatCard from "../../components/ui/StatCard"
// import Badge from "../../components/ui/Badge"

// const API = "/api"

// function isRecent(dateString, minutes = 60) {
//   if (!dateString) return false
//   const date = new Date(dateString.replace(" ", "T"))
//   if (isNaN(date.getTime())) return false
//   return (new Date() - date) / 60000 <= minutes
// }

// export default function Dashboard() {
//   const { user } = useAuth()

//   const [stats, setStats] = useState({})
//   const [colis, setColis] = useState([])
//   const [demandes, setDemandes] = useState([])
//   const [loading, setLoading] = useState(true)

//   useEffect(() => {
//     async function load() {
//       const [c, d, b, u, dep, f] = await Promise.all([
//         fetch(`${API}/colis/`).then(r => r.json()).catch(() => []),
//         fetch(`${API}/demande_achat/`).then(r => r.json()).catch(() => []),
//         fetch(`${API}/bon_commande/`).then(r => r.json()).catch(() => []),
//         fetch(`${API}/users/`).then(r => r.json()).catch(() => []),
//         fetch(`${API}/departement/`).then(r => r.json()).catch(() => []),
//         fetch(`${API}/fournisseur/`).then(r => r.json()).catch(() => []),
//       ])

//       setStats({
//         colis: c.length,
//         demandes: d.length,
//         bons: b.length,
//         users: u.length,
//         deps: dep.length,
//         fournis: f.length,
//       })

//       setColis(c.slice(0, 5))
//       setDemandes(d.filter(x => x.statut === "en_attente").slice(0, 5))

//       setLoading(false)
//     }

//     load()
//   }, [])

//   if (loading) {
//     return (
//       <div className="p-6 grid grid-cols-4 gap-4">
//         {Array(8).fill(0).map((_, i) => (
//           <div key={i} className="h-24 bg-gray-100 animate-pulse rounded-xl" />
//         ))}
//       </div>
//     )
//   }

//   return (
//     <div className="max-w-6xl mx-auto p-4">

//       {/* HEADER */}
//       <div className="mb-8 flex justify-between items-center">
//         <div>
//           <h1 className="text-3xl font-bold text-gray-900">
//             Tableau de bord
//           </h1>
//           <p className="text-gray-500 mt-1">
//             Bienvenue {user?.full_name}
//           </p>
//         </div>
//       </div>

//       {/* STATS */}
//       <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
//         <StatCard label="Colis" value={stats.colis} icon="📦" color="bg-indigo-50" />
//         <StatCard label="Demandes" value={stats.demandes} icon="📝" color="bg-yellow-50" />
//         <StatCard label="Bons" value={stats.bons} icon="📋" color="bg-blue-50" />
//         <StatCard label="Utilisateurs" value={stats.users} icon="👥" color="bg-green-50" />
//       </div>

//       {/* CONTENT */}
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">

//         {/* COLIS */}
//         <div className="bg-white rounded-2xl border p-5 shadow-sm">
//           <div className="flex justify-between mb-4">
//             <h2 className="font-semibold">Derniers colis</h2>
//             <Link to="/admin/colis" className="text-indigo-600 text-sm">
//               Voir tout
//             </Link>
//           </div>

//           <table className="w-full text-sm">
//             <tbody>
//               {colis.map(c => (
//                 <tr
//                   key={c.id_colis}
//                   className={`border-b last:border-0 hover:bg-gray-50 ${
//                     isRecent(c.date_creation) ? "bg-yellow-50" : ""
//                   }`}
//                 >
//                   <td className="py-2 font-mono text-xs">
//                     {c.numero_suivi}
//                   </td>
//                   <td className="py-2">{c.destinataire_nom}</td>
//                   <td className="py-2">
//                     <Badge statut={c.statut_libelle} />
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>

//         {/* DEMANDES */}
//         <div className="bg-white rounded-2xl border p-5 shadow-sm">
//           <div className="flex justify-between mb-4">
//             <h2 className="font-semibold">Demandes en attente</h2>
//             <Link to="/admin/demande_achat" className="text-indigo-600 text-sm">
//               Voir tout
//             </Link>
//           </div>

//           <table className="w-full text-sm">
//             <tbody>
//               {demandes.map(d => (
//                 <tr key={d.id_demande} className="border-b last:border-0 hover:bg-gray-50">
//                   <td className="py-2">{d.objet}</td>
//                   <td className="py-2 text-gray-500">{d.demandeur_nom}</td>
//                   <td className="py-2">{d.montant_estime} €</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>

//       </div>
//     </div>
//   )
// }

import { useEffect, useState } from "react"
import { demandeAchatService } from "../../services/demandeService"

const API = "/api"

export default function DashboardDemandes() {
  const [demandes, setDemandes] = useState([])
  const [loading, setLoading] = useState(true)

useEffect(() => {
  async function load() {
    try {
      const d = await demandeAchatService.getAll()

      setDemandes(
        d.filter(x => x.statut === "en_attente")
      )
    } catch (e) {
      console.error(e.message)
    }
  }

  load()
}, [])

  if (loading) {
    return (
      <div className="p-6 space-y-3">
        <div className="h-6 w-40 bg-gray-100 animate-pulse rounded" />
        <div className="h-32 bg-gray-100 animate-pulse rounded-xl" />
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto p-4">

      {/* HEADER */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Demandes d'achat
          </h1>
          <p className="text-sm text-gray-500">
            Gestion des demandes en attente de validation
          </p>
        </div>

        <div className="bg-yellow-50 text-yellow-700 px-3 py-1 rounded-full text-sm font-medium">
          {demandes.length} en attente
        </div>
      </div>

      {/* MOBILE CARDS */}
      <div className="grid gap-3 sm:hidden">
        {demandes.map(d => (
          <div
            key={d.id_demande}
            className="p-4 bg-white border rounded-xl shadow-sm"
          >
            <div className="font-semibold text-gray-900">
              {d.objet}
            </div>

            <div className="text-sm text-gray-500 mt-1">
              {d.demandeur_nom}
            </div>

            <div className="mt-2 font-bold text-indigo-600">
              {d.montant_estime} €
            </div>
          </div>
        ))}
      </div>

      {/* TABLE DESKTOP */}
      <div className="hidden sm:block bg-white border rounded-2xl shadow-sm overflow-hidden">

        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              <th className="text-left p-3">Objet</th>
              <th className="text-left p-3">Demandeur</th>
              <th className="text-left p-3">Montant</th>
            </tr>
          </thead>

          <tbody>
            {demandes.map(d => (
              <tr
                key={d.id_demande}
                className="border-t hover:bg-gray-50 transition"
              >
                <td className="p-3 font-medium text-gray-900">
                  {d.objet}
                </td>

                <td className="p-3 text-gray-600">
                  {d.demandeur_nom}
                </td>

                <td className="p-3 font-semibold text-indigo-600">
                  {d.montant_estime} €
                </td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>
    </div>
  )
}

