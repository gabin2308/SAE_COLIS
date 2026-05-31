export default function Badge({ statut }) {
  const config = {
    en_attente: { label: "En attente", color: "bg-yellow-100 text-yellow-800" },
    approuvee: { label: "Approuvée", color: "bg-green-100 text-green-800" },
    refusee: { label: "Refusée", color: "bg-red-100 text-red-800" },
    en_preparation: { label: "Préparation", color: "bg-blue-100 text-blue-800" },
    envoye: { label: "Envoyé", color: "bg-indigo-100 text-indigo-800" },
    en_transit: { label: "En transit", color: "bg-purple-100 text-purple-800" },
    livre: { label: "Livré", color: "bg-emerald-100 text-emerald-800" },
    annule: { label: "Annulé", color: "bg-gray-100 text-gray-600" },
    accepte: { label: "Accepté", color: "bg-green-100 text-green-800" },
    refuse: { label: "Refusé", color: "bg-red-100 text-red-800" },
  }

  const current = config[statut] || {
    label: statut?.replaceAll("_", " ") || "Inconnu",
    color: "bg-gray-100 text-gray-600"
  }

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${current.color}`}
    >
      {current.label}
    </span>
  )
}