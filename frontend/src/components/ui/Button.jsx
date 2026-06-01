export default function Button({ children, variant = "primary", onClick, type = "button", disabled = false }) {
  const baseStyle = "px-5 py-2.5 rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition-all shadow-sm"
  
  const variants = {
    primary: "bg-gradient-to-r from-[#1a7fd4] to-[#0d5fa8] hover:opacity-90 text-white shadow-blue-500/10",
    secondary: "bg-white border-2 border-[#dde3ec] hover:border-slate-400 text-[#3d4f6e]"
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      {children}
    </button>
  )
}