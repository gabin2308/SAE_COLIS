import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { colisService } from "../../services/colisService"
import { useAuth } from "../../context/AuthContext"
import Card from "../../components/colis/Card" 
import StatusBadge from "../../components/ui/StatusBadge"
import Button from "../../components/colis/Button"

export default function Colis() {
  const { user } = useAuth()
  const navigate = useNavigate()
  
  const [colisList, setColisList] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const isAgent = ["administrateur", "postal_iut", "postal_univ"].includes(user?.role)
      const data = isAgent ? await colisService.getAll() : await colisService.getMesColis()
      setColisList(data || [])
    } catch (err) {
      alert("Impossible de charger les colis.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [user])

  const handleColisAction = async (id, action) => {
    try {
      if (action === 'receptionner') await colisService.receptionner(id)
      else if (action === 'transferer') await colisService.transfererIut(id)
      else if (action === 'retirer') await colisService.retirer(id)
      
      alert(`Action '${action}' effectuée avec succès.`)
      fetchData() // Recharge la liste pour mettre à jour les statuts
    } catch (err) {
      alert(`Échec de l'action : ${action}`)
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="flex items-center gap-4 mb-6">
        <button onClick={() => navigate("/dashboard")} className="text-slate-500 hover:text-[#0d2a4a] font-semibold">
          ← Retour
        </button>
        <h1 className="text-2xl font-bold text-[#0d2a4a]">Gestion des Colis</h1>
      </div>

      {loading ? (
        <p className="text-center py-10">Chargement des colis...</p>
      ) : (
        <div className="space-y-4">
          {colisList.length === 0 ? (
            <p className="text-center text-slate-400 py-10">Aucun colis trouvé.</p>
          ) : (
            colisList.map(c => (
              <Card key={c.id_colis || c.id} title={`Colis #${c.numero_suivi}`}>
                <div className="flex justify-between items-center">
                  <StatusBadge status={c.statut_libelle} />
                  
                  {/* Actions réservées aux agents */}
                  {["administrateur", "postal_iut", "postal_univ"].includes(user?.role) && (
                    <div className="flex gap-2">
                      {c.statut_libelle === 'recu_universite' && (
                        <Button variant="primary" onClick={() => handleColisAction(c.id_colis, 'receptionner')}>
                          Réceptionner
                        </Button>
                      )}
                      {c.statut_libelle === 'disponible' && (
                        <Button variant="success" onClick={() => handleColisAction(c.id_colis, 'retirer')}>
                          Retirer
                        </Button>
                      )}
                      {c.statut_libelle !== 'retire' && (
                        <Button variant="danger" onClick={() => handleColisAction(c.id_colis, 'transferer')}>
                          Transférer
                        </Button>
                      )}
                    </div>
                  )}
                </div>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  )
}