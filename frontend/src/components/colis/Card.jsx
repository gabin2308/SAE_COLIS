export default function Card({ title, actionText, onActionClick, children }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      {(title || actionText) && (
        <div className="flex justify-between items-center mb-4">
          {title && <h3 className="font-bold text-[#0d2a4a]">{title}</h3>}
          {actionText && (
            <button onClick={onActionClick} className="text-xs text-[#0d4f8a] font-semibold hover:underline">
              {actionText}
            </button>
          )}
        </div>
      )}
      {children}
    </div>
  )
}