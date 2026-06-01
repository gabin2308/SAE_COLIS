import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { demandeService } from "../../services/demandeService"
import { useAuth } from "../../context/AuthContext"
import Card from "../../components/ui/Card"
import Button from "../../components/ui/Button"
import StatusBadge from "../../components/ui/StatusBadge"

export default function Demandes() {
  const { user } = useAuth()
  const navigate = useNavigate()
  
  const [demandes, setDemandes] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const data = user?.role === "administrateur" 
        ? await demandeService.getAll() 
        : await demandeService.getMesDemandes()
      
      setDemandes(data || [])
    } catch (err) {
      console.error("Erreur chargement :", err)
      alert("Erreur lors du chargement des demandes.")
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (item, action) => {
    const id = item.id_demande || item.id || item._id;

    if (!id) {
      alert("Identifiant introuvable.");
      return;
    }

    try {
      if (action === 'approuver') {
        await demandeService.approuver(id, "");
      } else {
        const motif = prompt("Motif du refus :") || "Refusé par administrateur";
        await demandeService.refuser(id, motif);
      }
      
      alert(`Demande ${action}e avec succès.`);
      fetchData(); 
    } catch (err) {
      console.error("Erreur API :", err)
      alert("Une erreur est survenue lors de l'action.")
    }
  }

  useEffect(() => { fetchData() }, [])

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      {/* Bouton retour ajouté ici */}
      <button 
        onClick={() => navigate("/dashboard")} 
        className="text-slate-500 hover:text-[#0d2a4a] font-semibold mb-6 transition-colors"
      >
        ← Retour au tableau de bord
      </button>

      <h1 className="text-2xl font-bold mb-6">Gestion des Demandes</h1>
      
      {loading ? <p className="text-center py-10">Chargement...</p> : (
        <div className="space-y-4">
          {demandes.length > 0 ? (
            demandes.map(d => (
              <Card key={`demande-${d.id_demande || d.id || d._id}`} title={d.objet}>
                <div className="flex justify-between items-center">
                  <p className="text-slate-600">{d.description}</p>
                  
                  <div className="flex gap-2 items-center">
                    {user?.role === 'administrateur' && d.statut === 'en_attente' && (
                      <>
                        <Button variant="success" onClick={() => handleAction(d, 'approuver')}>Approuver</Button>
                        <Button variant="danger" onClick={() => handleAction(d, 'refuser')}>Refuser</Button>
                      </>
                    )}
                    <StatusBadge status={d.statut} />
                  </div>
                </div>
              </Card>
            ))
          ) : (
            <p className="text-center text-slate-400 py-10">Aucune demande trouvée.</p>
          )}
        </div>
      )}
    </div>
  )
}