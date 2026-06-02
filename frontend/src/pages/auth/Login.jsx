import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"
import logoIut from "../../assets/logo-iutv.png"
import logoSorb from "../../assets/sorbonne.png"
import { Eye, EyeOff, Loader2, AlertCircle } from "lucide-react"

export default function Login() {
  const [email, setEmail]       = useState("")
  const [password, setPassword] = useState("")
  const [showPwd, setShowPwd]   = useState(false)
  const [error, setError]       = useState(null)
  const [loading, setLoading]   = useState(false)

  const navigate = useNavigate()
  const { login } = useAuth()

  const handleLogin = async (e) => {
    if (e) e.preventDefault()
    setError(null)

    if (!email || !password) {
      setError("Veuillez remplir tous les champs")
      return
    }

    setLoading(true)
    const result = await login(email, password)

    if (result.success) {
      navigate("/dashboard")
    } else {
      setError(result.error || "Identifiants invalides")
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen font-sans">

      {/* ── Partie gauche ── */}
      <div className="hidden lg:flex flex-1 relative items-end p-12"
        style={{ background: "linear-gradient(160deg, #0d6ebd 0%, #1a9fd4 50%, #0a4f8a 100%)" }}
      >
        {/* Overlay */}
        <div className="absolute inset-0" style={{ background: "rgba(5,40,80,0.38)" }} />

        {/* Motif décoratif */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-24 -right-24 w-96 h-96 rounded-full opacity-10"
            style={{ background: "radial-gradient(circle, white, transparent)" }} />
          <div className="absolute top-1/3 -left-16 w-64 h-64 rounded-full opacity-10"
            style={{ background: "radial-gradient(circle, white, transparent)" }} />
          <div className="absolute bottom-32 right-24 w-48 h-48 rounded-full opacity-10"
            style={{ background: "radial-gradient(circle, white, transparent)" }} />
        </div>

        {/* Texte bas gauche */}
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-6">
            <span className="w-8 h-0.5 bg-white/60" />
            <span className="text-white/60 text-xs font-medium uppercase tracking-widest">SAE Colis</span>
          </div>
          <h2 className="text-white text-3xl font-light leading-snug mb-4">
            Système de gestion<br />
            <span className="font-bold">des colis et commandes</span>
          </h2>
          <p className="text-white/60 text-sm max-w-xs leading-relaxed">
            Plateforme de suivi des colis, demandes d'achat et bons de commande de l'IUT de Villetaneuse.
          </p>

          {/* Indicateurs feature */}
          <div className="flex gap-4 mt-8">
            {["Suivi colis", "Bons commande", "Devis"].map(f => (
              <div key={f} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-sky-300" />
                <span className="text-white/70 text-xs">{f}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Partie droite ── */}
      <div className="w-full lg:w-[480px] flex items-center justify-center bg-[#f7f9fc] px-6 py-10">
        <div className="w-full max-w-sm">

          {/* Logos */}
          <div className="flex items-center gap-4 mb-10">
            <img src={logoIut}  alt="IUT Villetaneuse" className="h-12 object-contain" />
            <div className="w-px h-10 bg-slate-200" />
            <img src={logoSorb} alt="Sorbonne Paris Nord" className="h-16 object-contain" />
          </div>

          {/* Titre */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[#0d2a4a] mb-1">Connexion</h1>
            <p className="text-sm text-slate-500">Espace personnel IUT Villetaneuse</p>
          </div>

          {/* Erreur */}
          {error && (
            <div className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-xl px-4 py-3 mb-6">
              <AlertCircle size={16} className="text-red-500 mt-0.5 shrink-0" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Formulaire */}
          <div className="space-y-5">

            {/* Email */}
            <div>
              <label className="block text-xs font-semibold text-[#3d4f6e] mb-1.5">
                Adresse email
              </label>
              <input
                type="email"
                placeholder="prenom.nom@iutv.univ-paris13.fr"
                value={email}
                onChange={e => setEmail(e.target.value)}
                onKeyDown={e => e.key === "Enter" && handleLogin()}
                className="w-full px-4 py-3 text-sm border border-slate-200 rounded-xl outline-none text-[#0d2a4a] placeholder:text-slate-400 focus:border-[#0d4f8a] focus:ring-2 focus:ring-[#0d4f8a]/10 transition-all"
              />
            </div>

            {/* Mot de passe */}
            <div>
              <label className="block text-xs font-semibold text-[#3d4f6e] mb-1.5">
                Mot de passe
              </label>
              <div className="relative">
                <input
                  type={showPwd ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && handleLogin()}
                  className="w-full px-4 py-3 pr-11 text-sm border border-slate-200 rounded-xl outline-none text-[#0d2a4a] placeholder:text-slate-400 focus:border-[#0d4f8a] focus:ring-2 focus:ring-[#0d4f8a]/10 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPwd(v => !v)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                >
                  {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Bouton */}
            <button
              onClick={handleLogin}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-semibold text-white transition-all disabled:opacity-70 disabled:cursor-not-allowed hover:opacity-90 active:scale-[0.99]"
              style={{ background: "linear-gradient(135deg, #1a7fd4, #0d5fa8)" }}
            >
              {loading
                ? <><Loader2 size={16} className="animate-spin" /> Connexion en cours...</>
                : "Se connecter"
              }
            </button>
          </div>

          {/* Footer */}
          <p className="text-center text-xs text-slate-400 mt-10">
            IUT de Villetaneuse · Université Sorbonne Paris Nord
          </p>
        </div>
      </div>
    </div>
  )
}