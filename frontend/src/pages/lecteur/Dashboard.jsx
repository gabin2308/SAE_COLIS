// import { useState, useEffect } from "react"
// import { useNavigate } from "react-router-dom"
// import { useAuth } from "../../context/AuthContext"
// import { useNotification } from "../../context/NotificationContext"
// import { colisService } from "../../services/colisService"
// import { demandeService } from "../../services/demandeService"
// import Header from '../../components/ui/Header'
// import WelcomeRow from "../../components/ui/WelcomeRow"
// import Card from "../../components/ui/Card"
// import StatusBadge from "../../components/ui/StatusBadge"

// export default function Dashboard() {
//   const { user } = useAuth()
//   const { unreadCount } = useNotification() // Compteur pour le badge
//   const navigate = useNavigate()

//   const [allColis, setAllColis] = useState([])
//   const [filteredColis, setFilteredColis] = useState([])
//   const [demandes, setDemandes] = useState([])
//   const [searchSuivi, setSearchSuivi] = useState("")
//   const [loading, setLoading] = useState(true)

//   const loadData = async () => {
//     setLoading(true)
//     try {
//       const isAgent = ["administrateur", "postal_iut", "postal_univ"].includes(user?.role)
//       const [colisData, demandesData] = await Promise.all([
//         isAgent ? colisService.getAll() : colisService.getMesColis(),
//         user?.role === "administrateur" ? demandeService.getAll() : demandeService.getMesDemandes()
//       ])

//       setAllColis(colisData || [])
//       setFilteredColis((colisData || []).slice(0, 5))
//       setDemandes(demandesData || [])
//     } catch (err) {
//       console.error("Erreur chargement dashboard", err)
//     } finally {
//       setLoading(false)
//     }
//   }

//   useEffect(() => { loadData() }, [user])

//   const handleSearchChange = (e) => {
//     const value = e.target.value
//     setSearchSuivi(value)
//     if (!value) {
//       setFilteredColis(allColis.slice(0, 5))
//     } else {
//       const filtered = allColis.filter(c => 
//         c.numero_suivi?.toLowerCase().includes(value.toLowerCase())
//       )
//       setFilteredColis(filtered.slice(0, 5))
//     }
//   }

//   return (
//     <div className="min-h-screen bg-[#f7f9fc] font-sans text-[#0d2a4a]">
//       {/* Passage du compteur unreadCount au Header */}
//       <Header notifCount={unreadCount} />

//       <main className="max-w-7xl mx-auto p-4 md:p-8">
//         <WelcomeRow 
//           prenom={user?.prenom} 
//           onScanClick={() => navigate("/scan")} 
//           onNewDemandeClick={() => navigate("/demandes/nouvelle")}
//         />

//         {/* Barre de recherche et bouton refresh */}
//         <div className="flex gap-2 bg-white p-2 rounded-xl shadow-sm border border-slate-100 mb-8">
//           <input 
//             type="text" 
//             placeholder="Recherche rapide par numéro de suivi..." 
//             value={searchSuivi}
//             onChange={handleSearchChange}
//             className="flex-1 border-none outline-none px-3 py-2 text-sm text-[#0d2a4a] placeholder-slate-400"
//           />
//           <button 
//             onClick={loadData}
//             className="bg-[#0d4f8a] hover:bg-[#0a3f6e] text-white px-4 md:px-6 rounded-lg text-sm font-semibold transition-colors"
//           >
//             🔄
//           </button>
//         </div>

//         {loading ? (
//           <div className="text-center text-slate-500 py-12">Chargement...</div>
//         ) : (
//           <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
//             <Card title="📦 Colis récents" actionText="Voir tout" onActionClick={() => navigate("/colis")}>
//               {filteredColis.length === 0 ? (
//                 <p className="text-sm text-slate-400 text-center py-8">Aucun colis trouvé.</p>
//               ) : (
//                 <div className="space-y-3">
//                   {filteredColis.map((c) => (
//                     <div key={c.id_colis || c.id} className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100">
//                       <div>
//                         <div className="text-sm font-semibold">{c.numero_suivi}</div>
//                         <div className="text-xs text-slate-400">BC: #{c.bon_commande_id}</div>
//                       </div>
//                       <StatusBadge status={c.statut_libelle} />
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </Card>

//             <Card title="📄 Demandes d'Achat" actionText="Voir tout" onActionClick={() => navigate("/demande")}>
//               {demandes.length === 0 ? (
//                 <p className="text-sm text-slate-400 text-center py-8">Aucune demande.</p>
//               ) : (
//                 <div className="space-y-3">
//                   {demandes.slice(0, 5).map((d) => (
//                     <div key={d.id} className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100">
//                       <div className="truncate max-w-[60%]">
//                         <div className="text-sm font-semibold truncate">{d.description}</div>
//                         <div className="text-xs text-slate-400">
//                           {new Date(d.date_creation).toLocaleDateString("fr-FR")}
//                         </div>
//                       </div>
//                       <StatusBadge status={d.statut} />
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </Card>
//           </div>
//         )}
//       </main>
//     </div>
//   )
// }
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"
import { colisService } from "../../services/colisService"
import { demandeService } from "../../services/demandeService"
import Header from '../../components/ui/Header'
import WelcomeRow from "../../components/ui/WelcomeRow"
import Card from "../../components/ui/Card"
import StatusBadge from "../../components/ui/StatusBadge"

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [allColis, setAllColis] = useState([])
  const [filteredColis, setFilteredColis] = useState([])
  const [demandes, setDemandes] = useState([])
  const [searchSuivi, setSearchSuivi] = useState("")
  const [loading, setLoading] = useState(true)

  const loadData = async () => {
    setLoading(true)
    try {
      const isAgent = ["administrateur", "postal_iut", "postal_univ"].includes(user?.role)
      const [colisData, demandesData] = await Promise.all([
        isAgent ? colisService.getAll() : colisService.getMesColis(),
        user?.role === "administrateur" ? demandeService.getAll() : demandeService.getMesDemandes()
      ])

      setAllColis(colisData || [])
      setFilteredColis((colisData || []).slice(0, 5))
      setDemandes(demandesData || [])
    } catch (err) {
      console.error("Erreur chargement dashboard", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadData() }, [user])

  const handleSearchChange = (e) => {
    const value = e.target.value
    setSearchSuivi(value)
    if (!value) {
      setFilteredColis(allColis.slice(0, 5))
    } else {
      const filtered = allColis.filter(c => 
        c.numero_suivi?.toLowerCase().includes(value.toLowerCase())
      )
      setFilteredColis(filtered.slice(0, 5))
    }
  }

  return (
    <div className="min-h-screen bg-[#f7f9fc] font-sans text-[#0d2a4a]">
      {/* Header sans props de notification */}
      <Header />

      <main className="max-w-7xl mx-auto p-4 md:p-8">
        <WelcomeRow 
          prenom={user?.prenom} 
          onScanClick={() => navigate("/scan")} 
          onNewDemandeClick={() => navigate("/demandes/nouvelle")}
        />

        <div className="flex gap-2 bg-white p-2 rounded-xl shadow-sm border border-slate-100 mb-8">
          <input 
            type="text" 
            placeholder="Recherche rapide par numéro de suivi..." 
            value={searchSuivi}
            onChange={handleSearchChange}
            className="flex-1 border-none outline-none px-3 py-2 text-sm text-[#0d2a4a] placeholder-slate-400"
          />
          <button 
            onClick={loadData}
            className="bg-[#0d4f8a] hover:bg-[#0a3f6e] text-white px-4 md:px-6 rounded-lg text-sm font-semibold transition-colors"
          >
            🔄
          </button>
        </div>

        {loading ? (
          <div className="text-center text-slate-500 py-12">Chargement...</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <Card title="📦 Colis récents" actionText="Voir tout" onActionClick={() => navigate("/colis")}>
              {filteredColis.length === 0 ? (
                <p className="text-sm text-slate-400 text-center py-8">Aucun colis trouvé.</p>
              ) : (
                <div className="space-y-3">
                  {filteredColis.map((c) => (
                    <div key={`colis-${c.id_colis || c.id}`} className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100">
                      <div>
                        <div className="text-sm font-semibold">{c.numero_suivi}</div>
                        <div className="text-xs text-slate-400">BC: #{c.bon_commande_id}</div>
                      </div>
                      <StatusBadge status={c.statut_libelle} />
                    </div>
                  ))}
                </div>
              )}
            </Card>

            <Card title="📄 Demandes d'Achat" actionText="Voir tout" onActionClick={() => navigate("/demande")}>
              {demandes.length === 0 ? (
                <p className="text-sm text-slate-400 text-center py-8">Aucune demande.</p>
              ) : (
                <div className="space-y-3">
                  {demandes.slice(0, 5).map((d) => (
                    <div key={`demande-${d.id}`} className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100">
                      <div className="truncate max-w-[60%]">
                        <div className="text-sm font-semibold truncate">{d.description}</div>
                        <div className="text-xs text-slate-400">
                          {new Date(d.date_creation).toLocaleDateString("fr-FR")}
                        </div>
                      </div>
                      <StatusBadge status={d.statut} />
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>
        )}
      </main>
    </div>
  )
}