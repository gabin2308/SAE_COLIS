
export function DashCard({ icon, title, count, onAction, accentClass, children }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
      <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <span className={`p-1.5 rounded-lg ${accentClass}`}>{icon}</span>
          <h2 className="font-semibold text-[#0d2a4a] text-sm">{title}</h2>
          {count > 0 && (
            <span className="text-xs font-bold bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">
              {count}
            </span>
          )}
        </div>
        <button
          onClick={onAction}
          className="text-xs font-semibold text-[#0d4f8a] hover:underline"
        >
          Voir tout →
        </button>
      </div>
      <div className="px-5 py-4 space-y-2">
        {children}
      </div>
    </div>
  )
}

export function Empty({ text }) {
  return (
    <p className="text-slate-400 text-sm italic py-3 text-center">
      {text}
    </p>
  )
}