import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"
import logoIut from "../../assets/logo-iutv.png"
import logoSorb from "../../assets/sorbonne.png"
// Constantes pour les logos (utilisez vos chaînes base64 ici)
// 1. Définissez vos constantes en haut de votre fichier
// 1. Définissez vos constantes en haut de votre fichier

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  
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
    <div style={styles.page}>
      {/* Partie gauche */}
      <div style={styles.left}>
        <div style={styles.overlay} />
        <div style={styles.leftContent}>
          <p style={styles.tagline}>Système de gestion<br />des colis et commandes</p>
        </div>
      </div>

      {/* Partie droite (Formulaire) */}
      <div style={styles.right}>
        <div style={styles.card}>
          <div style={styles.logos}>
            <img src={logoIut} alt="IUT" style={styles.logoIut} />
            <div style={styles.logoDivider} />
            <img src={logoSorb} alt="Sorbonne" style={styles.logoSorb} />
          </div>

          <h1 style={styles.title}>Connexion</h1>
          <p style={styles.subtitle}>Espace personnel IUT Villetaneuse</p>

          {error && (
            <div style={styles.errorBox}>
              <span style={{ fontSize: 16, marginRight: 8 }}>⚠</span>{error}
            </div>
          )}

          <div style={styles.field}>
            <label style={styles.label}>Adresse email</label>
            <input
              type="email"
              placeholder="prenom.nom@iutv.univ-paris13.fr"
              value={email}
              onChange={e => setEmail(e.target.value)}
              style={styles.input}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Mot de passe</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleLogin()}
              style={styles.input}
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading}
            style={{ ...styles.btn, opacity: loading ? 0.7 : 1 }}
          >
            {loading ? "Connexion..." : "Se connecter"}
          </button>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: { display: "flex", minHeight: "100vh", fontFamily: "'Segoe UI', sans-serif" },
  left: { flex: 1, background: "linear-gradient(160deg, #0d6ebd 0%, #1a9fd4 50%, #0a4f8a 100%)", position: "relative", display: "flex", alignItems: "flex-end", padding: "3rem" },
  overlay: { position: "absolute", inset: 0, background: "rgba(5, 40, 80, 0.35)" },
  leftContent: { position: "relative", zIndex: 1 },
  tagline: { color: "white", fontSize: "1.5rem", fontWeight: 300, margin: 0 },
  right: { width: "460px", display: "flex", alignItems: "center", justifyContent: "center", background: "#f7f9fc", padding: "2rem" },
  card: { width: "100%", maxWidth: "380px", background: "#fff", borderRadius: "16px", padding: "2.5rem 2rem", boxShadow: "0 4px 24px rgba(0,0,0,0.08)" },
  logos: { display: "flex", alignItems: "center", gap: "1rem", marginBottom: "2rem" },
  logoIut: { height: "52px", objectFit: "contain" },
  logoDivider: { width: "1px", height: "40px", background: "#dde3ec" },
  logoSorb: { height: "70px", objectFit: "contain" },
  title: { fontSize: "1.5rem", fontWeight: 700, color: "#0d2a4a", margin: "0 0 0.25rem" },
  subtitle: { fontSize: "0.875rem", color: "#6b7a99", margin: "0 0 1.75rem" },
  errorBox: { background: "#fff3f3", border: "1px solid #fbc5c5", borderRadius: "8px", padding: "0.75rem 1rem", fontSize: "0.875rem", color: "#c0392b", marginBottom: "1.25rem", display: "flex", alignItems: "center" },
  field: { marginBottom: "1.25rem" },
  label: { display: "block", fontSize: "0.8125rem", fontWeight: 600, color: "#3d4f6e", marginBottom: "0.4rem" },
  input: { width: "100%", padding: "0.65rem 0.875rem", border: "1.5px solid #dde3ec", borderRadius: "8px", outline: "none", color: "#0d2a4a" },
  btn: { width: "100%", padding: "0.75rem", fontWeight: 600, background: "linear-gradient(135deg, #1a7fd4, #0d5fa8)", color: "#fff", border: "none", borderRadius: "8px", cursor: "pointer", marginTop: "0.5rem" }
}