export default function StatusBadge({ status }) {
  // Mapping complet de tes statuts (API Flask) vers les classes Tailwind
  const config = {
    // Statuts Colis
    recu_universite: "bg-blue-50 text-blue-700 border-blue-200",
    transfere_iut: "bg-amber-50 text-amber-700 border-amber-200",
    receptionne_iut: "bg-emerald-50 text-emerald-700 border-emerald-200",
    retire: "bg-slate-100 text-slate-700 border-slate-200",
    incident: "bg-rose-50 text-rose-700 border-rose-200",
    
    // Statuts Demandes d'Achat
    en_attente: "bg-amber-50 text-amber-600 border-amber-200",
    approuve: "bg-emerald-50 text-emerald-700 border-emerald-200",
    refuse: "bg-rose-50 text-rose-700 border-rose-200",
  }

  const currentClass = config[status] || "bg-slate-100 text-slate-700 border-slate-200"

  return (
    <span className={`text-[11px] font-bold px-2.5 py-1 rounded-full border tracking-wide capitalize whitespace-nowrap ${currentClass}`}>
      {status?.replace('_', ' ')}
    </span>
  )
}