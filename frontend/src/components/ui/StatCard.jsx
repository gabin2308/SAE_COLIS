export default function StatCard({ label, value, icon, color, trend }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-all duration-200">

      <div className="flex items-center justify-between">
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${color}`}>
          {icon}
        </div>

        {trend && (
          <span className="text-xs px-2 py-1 rounded-full bg-green-50 text-green-600 font-medium">
            {trend}
          </span>
        )}
      </div>

      <div className="mt-4">
        <p className="text-sm text-gray-500">{label}</p>

        <p className="text-3xl font-bold text-gray-900 mt-1">
          {value ?? "—"}
        </p>
      </div>
    </div>
  )
}