export default function Card({ title, actionText, onActionClick, children }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100/50">
      {title && (
        <div className="flex justify-between items-center mb-6 border-b border-slate-100 pb-3">
          <h2 className="text-lg font-bold text-[#0d2a4a]">{title}</h2>
          {actionText && onActionClick && (
            <span 
              onClick={onActionClick} 
              className="text-sm font-semibold text-[#1a7fd4] hover:text-[#0d5fa8] cursor-pointer transition-colors"
            >
              {actionText}
            </span>
          )}
        </div>
      )}
      {children}
    </div>
  )
}