import Button from "./Button"
import { useAuth } from "../../context/AuthContext"

export default function WelcomeRow({ 
  onScanClick, 
  onNewDemandeClick 
}) {

  const { user } = useAuth()
  return (
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      {/* Textes de bienvenue */}
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-[#0d2a4a]">
          Bonjour, {user?.full_name || "utilisateur"} ! 👋
        </h1>
        <p className="text-sm text-[#6b7a99] mt-1">
          Espace logistique — IUT Villetaneuse
        </p>
      </div>
      
      {/* Boutons d'actions rapides */}
      <div className="flex flex-col sm:flex-row gap-3">
        {onScanClick && (
          <Button variant="secondary" onClick={onScanClick}>
            📷 Scanner QR
          </Button>
        )}
        {onNewDemandeClick && (
          <Button variant="primary" onClick={onNewDemandeClick}>
            ➕ Nouvelle Demande
          </Button>
        )}
      </div>
    </div>
  )
}