import StatCard from "./StatCard"

export default function DashboardStats({ stats }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">

      <StatCard
        label="Colis total"
        value={stats.colis}
        icon="📦"
        color="bg-indigo-50"
      />

      <StatCard
        label="Demandes d'achat"
        value={stats.demandes}
        icon="📝"
        color="bg-yellow-50"
      />

      <StatCard
        label="Bons de commande"
        value={stats.bons}
        icon="📋"
        color="bg-blue-50"
      />

      <StatCard
        label="Utilisateurs"
        value={stats.users}
        icon="👥"
        color="bg-green-50"
      />

      <StatCard
        label="Départements"
        value={stats.deps}
        icon="🏢"
        color="bg-purple-50"
      />

      <StatCard
        label="Fournisseurs"
        value={stats.fournis}
        icon="🏭"
        color="bg-orange-50"
      />

      <StatCard
        label="Notifs non lues"
        value={stats.nonLues}
        icon="🔔"
        color="bg-red-50"
      />

    </div>
  )
}