export default function Badge({ statut }) {
  const styles = {
    en_attente: "bg-yellow-100 text-yellow-700",
    approuvee: "bg-green-100 text-green-700",
    refusee: "bg-red-100 text-red-700",
    en_preparation: "bg-blue-100 text-blue-700",
    envoye: "bg-indigo-100 text-indigo-700",
    en_transit: "bg-purple-100 text-purple-700",
    livre: "bg-green-100 text-green-700",
    annule: "bg-gray-100 text-gray-500",
    accepte: "bg-green-100 text-green-700",
    refuse: "bg-red-100 text-red-700",
  }

  const className =
    styles[statut] ?? "bg-gray-100 text-gray-500"

  const label =
    statut?.replaceAll("_", " ") ?? "inconnu"

  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${className}`}>
      {label}
    </span>
  )
}