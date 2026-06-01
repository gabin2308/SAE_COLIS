export default function Button({ children, onClick, variant = "primary", className = "" }) {
  const base = "px-4 py-2 rounded-lg text-sm font-semibold transition-all";
  const variants = {
    primary: "bg-blue-100 text-blue-700 hover:bg-blue-200",
    danger: "bg-orange-100 text-orange-700 hover:bg-orange-200",
    success: "bg-green-100 text-green-700 hover:bg-green-200"
  };

  return (
    <button onClick={onClick} className={`${base} ${variants[variant]} ${className}`}>
      {children}
    </button>
  )
}