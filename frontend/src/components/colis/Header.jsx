export default function Header({ notifCount }) {
  return (
    <header className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center">
      <div className="font-bold text-xl text-[#0d4f8a]">UniColis</div>
      <div className="relative">
        🔔 {notifCount > 0 && <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">{notifCount}</span>}
      </div>
    </header>
  )
}