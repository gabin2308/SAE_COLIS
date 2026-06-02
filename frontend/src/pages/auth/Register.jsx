import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authService } from "../../services/authService";
import { departementService } from "../../services/departementService"; // Assurez-vous d'utiliser ce service si nécessaire

// Constantes pour les logos (encodage Base64 conservé)
const LOGO_IUT = "data:image/png;base64,..."; 
const LOGO_SORB = "data:image/png;base64,...";

export default function Register() {
  const navigate = useNavigate();

  // États du formulaire
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    departementId: "",
    roleId: ""
  });

  const [departements, setDepartements] = useState([]);
  const [roles, setRoles] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Chargement des données (départements et rôles)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [depRes, roleRes] = await Promise.all([
          fetch("/api/departement/", { credentials: "include" }),
          fetch("/api/role/", { credentials: "include" })
        ]);
        
        const depData = await depRes.json();
        const roleData = await roleRes.json();
        
        setDepartements(Array.isArray(depData) ? depData : []);
        setRoles(Array.isArray(roleData) ? roleData : []);
      } catch (err) {
        console.error("Erreur de chargement des listes", err);
      }
    };
    fetchData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    // Validations
    if (Object.values(formData).some(val => val === "")) {
      return setError("Veuillez remplir tous les champs.");
    }
    if (formData.password.length < 8) {
      return setError("Le mot de passe doit faire au moins 8 caractères.");
    }
    if (formData.password !== formData.confirmPassword) {
      return setError("Les mots de passe ne correspondent pas.");
    }

    setLoading(true);
    try {
      const data = await authService.register(
        formData.fullName, 
        formData.email, 
        formData.password, 
        parseInt(formData.roleId), 
        parseInt(formData.departementId)
      );

      if (data.message) {
        navigate("/login");
      } else {
        setError(data.error || "Une erreur est survenue lors de l'inscription.");
      }
    } catch (err) {
      setError("Erreur de connexion au serveur.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.left}>
        <div style={styles.overlay} />
        <div style={styles.leftContent}>
          <p style={styles.tagline}>Rejoignez le système<br />de gestion IUT</p>
        </div>
      </div>

      <div style={styles.right}>
        <form style={styles.card} onSubmit={handleRegister}>
          <div style={styles.logos}>
            <img src={LOGO_IUT} alt="IUT Villetaneuse" style={styles.logoIut} />
            <div style={styles.logoDivider} />
            <img src={LOGO_SORB} alt="Sorbonne Paris Nord" style={styles.logoSorb} />
          </div>

          <h1 style={styles.title}>Créer un compte</h1>
          <p style={styles.subtitle}>Compte enseignant — rôle lecteur par défaut</p>

          {error && <div style={styles.errorBox}>⚠ {error}</div>}

          <div style={styles.field}>
            <label style={styles.label}>Nom complet</label>
            <input name="fullName" type="text" placeholder="Prénom Nom" onChange={handleChange} style={styles.input} required />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Adresse email</label>
            <input name="email" type="email" placeholder="prenom.nom@iutv.univ-paris13.fr" onChange={handleChange} style={styles.input} required />
          </div>

          <div style={styles.row}>
            <div style={{...styles.field, flex: 1}}>
              <label style={styles.label}>Mot de passe</label>
              <input name="password" type="password" placeholder="8 caractères min" onChange={handleChange} style={styles.input} required />
            </div>
            <div style={{...styles.field, flex: 1}}>
              <label style={styles.label}>Confirmer</label>
              <input name="confirmPassword" type="password" placeholder="••••••••" onChange={handleChange} style={styles.input} required />
            </div>
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Département</label>
            <select name="departementId" onChange={handleChange} style={styles.select} required>
              <option value="">-- Choisir un département --</option>
              {departements.map(d => <option key={d.id_departement} value={d.id_departement}>{d.nom}</option>)}
            </select>
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Rôle</label>
            <select name="roleId" onChange={handleChange} style={styles.select} required>
              <option value="">-- Choisir un rôle --</option>
              {roles.map(r => <option key={r.id_role} value={r.id_role}>{r.nom}</option>)}
            </select>
          </div>

          <button type="submit" disabled={loading} style={styles.btn}>
            {loading ? "Création..." : "Créer mon compte"}
          </button>

          <p style={styles.loginLink}>
            Déjà un compte ? <Link to="/" style={styles.link}>Se connecter</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

const styles = {
  // Vos styles originaux restent ici...
  page: { display: "flex", minHeight: "100vh", fontFamily: "'Segoe UI', sans-serif" },
  left: { flex: 1, background: "linear-gradient(160deg, #0d6ebd 0%, #1a9fd4 50%, #0a4f8a 100%)", position: "relative", display: "flex", alignItems: "flex-end", padding: "3rem" },
  overlay: { position: "absolute", inset: 0, background: "rgba(5,40,80,0.35)" },
  leftContent: { position: "relative", zIndex: 1 },
  tagline: { color: "#fff", fontSize: "1.5rem", fontWeight: 300 },
  right: { width: "500px", display: "flex", alignItems: "center", justifyContent: "center", background: "#f7f9fc", padding: "2rem" },
  card: { width: "100%", maxWidth: "440px", background: "#fff", borderRadius: "16px", padding: "2.5rem 2rem", boxShadow: "0 4px 24px rgba(0,0,0,0.08)" },
  logos: { display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1.75rem" },
  logoIut: { height: "52px" },
  logoDivider: { width: "1px", height: "40px", background: "#dde3ec" },
  logoSorb: { height: "70px" },
  title: { fontSize: "1.4rem", color: "#0d2a4a", margin: "0 0 0.25rem" },
  subtitle: { fontSize: "0.8125rem", color: "#6b7a99", marginBottom: "1.5rem" },
  errorBox: { background: "#fff3f3", border: "1px solid #fbc5c5", borderRadius: "8px", padding: "0.75rem", fontSize: "0.875rem", color: "#c0392b", marginBottom: "1rem" },
  field: { marginBottom: "1rem" },
  row: { display: "flex", gap: "0.75rem" },
  label: { display: "block", fontSize: "0.8125rem", fontWeight: 600, color: "#3d4f6e", marginBottom: "0.35rem" },
  input: { width: "100%", padding: "0.65rem", borderRadius: "8px", border: "1.5px solid #dde3ec", boxSizing: "border-box" },
  select: { width: "100%", padding: "0.65rem", borderRadius: "8px", border: "1.5px solid #dde3ec", cursor: "pointer" },
  btn: { width: "100%", padding: "0.75rem", border: "none", borderRadius: "8px", background: "#1a7fd4", color: "#fff", fontWeight: 600, cursor: "pointer" },
  loginLink: { textAlign: "center", fontSize: "0.8125rem", marginTop: "1.25rem" },
  link: { color: "#1a7fd4", fontWeight: 600, textDecoration: "none" }
};