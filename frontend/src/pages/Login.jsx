import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { authService } from "../services/authService"
import { useAuth } from "../context/AuthContext"
import usePageTitle  from "../hooks/usePagetitle"

const LOGO_IUT = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKUAAAClCAMAAAAK9c3oAAACAVBMVEUAAAB0wtcfss1TuNAEr8pjvtVpwNUNsMsDr8pxw9cMsMsJr8pVutIGr8oEr8pgvdRJutEDr8pyw9hywtdswdZXutIDr8oEr8oDr8phvtRxwtcEr8pywtdvwddzwtdov9Y3tM4psswDr8pwwtdMuNAEr8pHt89zw9dkvtRXu9JEts9RudEIr8ows81kvtR0w9cLsMtfvdQhssxqwNYossw7tM5Gt89ivdQFr8pivtRAtc4dscwss8xevdNqwNYMsMsSsMtMuNB0w9hbu9NHt9Bzw9cOsMs8tc4Nr8pGt89hvdRbvNM0tM1MuNAgsctkvtRywtcvs8wytM1zwtccsMtavNMDr8oCr8oMr8ofsMv09PT29vYpssw6tM4zs81Atc5MuNAjscxFts9WutJau9JSudFfvNMus8wAp8QasMsAosAUsMtkvtUAoL5pv9VIt89twdYAq8dwwdcnscwArck1tM1mv9VQudEApMJrwNYAqMU9tc7h7PAAqsZivtTv8vTD3uff6++IyNlgvdQAnLvy8vKs1OKj0d/x8/S12ON2w9fm7vGez97r8PLk7fFDtM0AmLeAxdeUy9zG3+h6w9YAmrm+3Oa52uUAlrSYzdzJ4Onb6e7W5uyMyNnY6O3M4urT5eum0uCExteo0+BywNRZudCv1uIUrsmRytux1uLQ5OseP56pAAAAV3RSTlMA/gz+8ycLLoaEXibZlHM6BvrnxWbi3M/Dl3VmWy303LaE6tK8m5eWfmtoRzo4Mh0dFhbx4dvasH744tnUzcG8sa+NhYBKR/r5+PHXzcvJvJyXb23lwk1tUJ9yAAAUV0lEQVR42uyXXU8TURCGt6UFLLaUltBC+bKC0GhQbECQiPhFTNRENJGSbKHfpOlmtylpSdPEG+/2VzvrMcy241k9dHfrxT6/4MmceWfmSB4eHh4ebrIdfJh5++DV2qfd3efAzs7H1dWTe1+Op55K/wfj05n5tbtj1UKhoGml0gWQz+fPgUtZvjo4Ogk98ksjJbqVefZhrFyuVk2SPZBsgyNIysXiGXBwFJmISqPBP/3mxX6lUikbltdgiZVss0rKV4ZlvZHL5d4nJkdRUlCs1WogySrJJEuDkmdAIwecAiAqucn47OG+ApJYSZQE+iUbhiQjkEy5VtDg5kpHUX6gZBUlSVOCJFoCc3tTkgtszWdVJlm7kQRQ8hwlAeZoJhCekBwm+DmrMkl87msj3hpKgiULjpEclEQC647Wc3sz2/0l+X0gOTTeRXNyqOeec+N+caXZVFVVUZQbSYCfHJSkzIUkR1iKN5vdrtrpsErSePd+V/ISByVKUpIOtGd0YbkFln1NSXcOSpKmpAQiUbsLedhikopJkj43IJMZxOelveX8GmOSnOTQGYTvbUk6ZeOq2WhxJTWyGElTWhL22zUj43+SLOM0x/fGGVRHSWsS9szOdzGTJNnepJIynUHWpL/ZMSR9PrA0ZhAuRiJJmjJHLPnMhIbPje4DR4sZVOpbjFBJMoP+TmRIyTu6ju9teQfReAswOZTka7Mk2TmYHJQsYlOKELZPUvQ4d6Oa+NxNq3j3OMe5W5oLOiZH4W3vPNDmx9vxCC3qpvfuDB7nGuc4x0oKE7rNMPfpPmxKIqlZxPv0dswcC0s+jv1DcnrkOCeWIqSfiJ6T9zE5RFLgOBcjIXh6bEBysJKYHMu/d500pSjrQpKzrJKCxzmRFCclcqstWyanBJDjHN97GAICd1ycSXa5d+8FIHCcC5AUGeeCx7khybl7nRruSz9ZNdMXp4EwjOONogiCgl88UMQDET+oCPpBEFQ8ESXJmG0arznCWEsiLe3GbqXtunR3Fdcq6nrf/6Uz6aZvm3SSIvN+DIX88h7PPDPTVQqLoVi9tZQbVHPDpPXON+d1gMyaHP01h5XxP825GlL/Srl+W6zmanPuJMw5lFtH7Fg9iV0TlDlCWU+t3q4IQxX6TdyxXRnmvDTenHu+Sxgjli7Otbnr+Y3/MOc45OHD+2Ue2rkAehbKdatyzDlAxpmkmFRnFxHqzjKiB9O8mLMCybMWxeQApKSE8z+/xj6jKJZY6OqANM0tOV2pnJyiypxb/Be6EwX6y6mZ+f7sgF9ld+bGCfbe0JSR7fXJEwkZUaLfVTeD0ShnRuANPoXuzdTKPHMerzmgQZitAspH3FJTUrPKsqLmxpCedWt1hq2MIOHkHFJ5d+zkSDm32Wug/MGoGjIM3i7NqGPpD4khqWVtyljB4w1j7njDobRVc4DSz6i4RcIGyoj2HF+hFJDuNfWF0+TmHCwlDl7OxdMzww0zi3IBQcQfBjGgtASlf1Q9O3BRMmrOSyqL4XqMPH3XRNEbP5BahmDSWnl5cTqO5kLE2GwOnix+ZZLR82QqXXuvanb2KXwvNOUopOG6Vf5jpkPInKhl4y9hmarumUPz3HqGBGWTsPhJKGe835SC0rbPKOZnawoysympKHbr9/KXnywkzPn2zWHEN7MpaySOsPc6oqxyAs9oPDquoLSPKgouxzsBqb69oxYmrY/tDq+6nmUSzonpJuQ7rZhUhuxmm0W5nC4TD1Q9bkrLFy/BipLvAw1S+V48ODmntsfJh/bPl2UsRaYWhiJRhtdPWkCiKNNEMo3Bc5/HlPAtUG9BiQtXxm93xO2dwpynx5ti2isttHGL+hFWIHutbJgrNLCYQAw/T1BCAQaQuFDYMHbnqDz/A3MOkEHvW7tb47Z4iemxTndRDGkTExpJjtOUw9z9w0bUkxIcPV+cZzRFCZCWbEoBWbg5jvJU/sk5QJZ779oLZY77OWJzbSSjT+lWX6Ao5rk/KphTSIboZQWlR4cgp/aM06HdE5tzmcn5NnrRwt4KZQdJ9WusUJIXff18lczlk+fR72YVuYR6S8ipE6vH6NCjiS/nbU9CPu6JTGmhBJMRiVBMeeHoGKchUgmQWSfnLu09Q6jzMqBaKAGSAuQT8U7ncJpyZ445h6Ys8J8ILfMaNvRS0pVU4oiy7jgH0pTXx0NCJmPIqWrYRQ2fFQw9lElIW5ZbhOPsT0Ee360+OQcN6m8YvyD0p+UbGilTTSlT6Zw8nto8noamzD61as0i9IkTqo0yredTEeXdS+uSlEceKpty2GJ4mDsIoTXcNvRRAuSg3uLVAuBIkvLQREdr1C+zZYTetEyqjRLqDfNdjyBLqSE/mGXO4R8jhdZHdAdhhg1tlKP1HkplqXg+JUSDyakkexKa0sOENBD6xamhjzKG9IelUqayWExJ0al8H2RRz2gJHuQyjZRerOd+st7F4rkk5e0ccx5BWix4jtAMDwy9lBSaEuotQFKCeVZxOV8YzqTLv4tUVritk3L8fJcE5YOrScrL9+7fK4p4cK9SGqtBlmf6JGhIrQyoVkpvZGWM9FxASpbNScrN9ytWICx3WKZOpejUx+29MX8nUvmMFwydlGAy8GgqK2nK7ZXKq/dLb369+lEIa+Wpu/XEwkhN06+xaXSnYdQsnZSWhEyIkJzvohiS7SnK0uP5r523X7qN7nTnaUCCuoMTdxA+fyxS+ZZRQyslNCXMd1Fm8h/rZv7bOBHF8ZRyH0IcQoA4xSkkTgkhJPgBCQkQ4hBCsj04DQ5sPB4zbQdPyWDqNAl2aZSDhNy9D6DQv5I3dghObANCfNXdTR1v8+m78ubN5NoXScprn5vS484vR1ft4OCIE74Rm/cCpc1pFSgH9H+krDHXWKjn383z+1o6ZTnsMQq2i/lvtaD5E8ZrW/F9bxtf7qDP2gyrWZR7/0S5lkoJQZnmb6g5Ccrboz4IVC5ygXvNYLtCvYKu/bnvrVjyB0OxZCmUFxFWHmvhKqwYfdtKrCHTKKOgNGOQsghJyi+TOT6v5nBjgRP39wB+Gi7ENsZINcxwOzlNI60IqyyMaKWLQpoxWRjBaXJqPKPU6RECNYEyvoiI+fsLoHx/mfKD2BsjqMj99Z3gCpMtY7bFqGFnB0LvUjgJSof+Fr38IKz3tme0Q8pjsTA3MMkvC5R7e6jD3Qx/S1N++eYy5ZOLfZBZMH0NolOjazNLmnSA5AszK0k5G1qjMxq6mHunIWXbw0ac0v9hTqlyfbVYXC1btub8Vc/nlTKC/PKjZcq3lo616Ft54h0ETYfm7ZDSpmOgvACOhAyxMRtgEhbWUjJG0Zg9freOSXNOqRhMYJCjL3dCM0hJWXptmfLpZHNeIAKs6RFTQmou3gbKTWomKVXGO+Hr730ePm3TaYRT9bk6zx3ehRybU4aNkGEkm4y5v4HygWXKtzeSfVCBuk1UI0IPvSpTAm1BFqdg0kaEdeJjEyijAATq4p/jDznY/hkuRoFBrPny25hBLtVzaclS6dllyueSx1o04ztalssHbkkQyBB06oJxkrLpYGam6QTrpuOKWkR9LHzbBBRTw8NN+C2jqxfETl1ESFPOIYHy+3sTq7PQkstnb3S/jtCRDz7ndITk5pitpEh1Mbh8lkCUCEW6PMLUfCqwoD4+k5AhPNol1vLkKhmUYMqvEquzG95LG+9rzO8jdElN1RWH8Cq/pVMqlt+LsACktV7JY/EnNRoPVourK7/KxEG/QpbJf6Qtk02GhIybsvJ6YqX7yqspk3NLNYm3F5xQZmNtByh/JmoqpcboyV97I9suo/MgnElCNn0zpGyImb+d7PwGf3/16Mu5ZT2WfqxlCxaNaIXqBMJKthPplIqJ8cF8c6rlq7YPb0eLQjWvWwlpq0KxkouIqPON+fsrKJeJUrRkyQhSsRg5QNuYkSMZVm4WJRR9fIWi5NjxhAGhMkVxTshCl3r5PUl5Jfh85mvGIBfyu/LVNw8kKZ8DyLRjLQ44D9UplovHE+JlUaoOIWdthMKGRLUVnfmVYwSaeb12TomJL5FUUzBdmnJh3LKY32DKb765N0n5/DvLHykBW4b5S45Rh9B9BAFFuQ3Xwq8FyTt1j16ene4g9EtY2jWVkl6/g6Q6/R6m3FE5n160Wrs/ce4Y0XgNlBGUX32zfmeS8rpXM86ca/4AoU1/Gyh3qYqxzrFquwsrNIt5QO9Yggrz5xXG1aiQe5R6Xw56gy88QrFuwX0KoSChO5aWlt/X4v5ef/TGXFKPzSEXP1JiuFBWRqIt2zbCflzjnKnq4i6J4bmhjR3FxYRw7c/LtoeFrJ+Y2UZ0iXMFFBuvbaX6uyJN+VouRZ8sH0qdtwm0hdqDbQivis+C7eEAkui0J4zI05KG/NTHIbYa/3+SG2TD1/yaHV9+RzPf7zL8vf5gGuVN8X3vBUoB3WtnByg3KGtcDM8Rxs06MSD0ONcATqe7bcHggaZw+GOrQCsf21YIq3G4GiKG2JahWbpzuQaWNPMF0ywWE/4OIb99OJemNzI/ECpOon7RwWs+xb0dF9d6xJBxRwk3bHNSP54IU9UxXMCOYFuMOC485gYY2hLwyNVlUHJNVXWoU1uKIFjPQxOLMXbNa9BkJPz97RO5VD2edZzbokchZZNhXin5M8q8EK3qaJMyha+cNI8qnka9i+rvl3Qz7+YHYPXqEWWaxunquH/mEoNbKyZXVV7e1Die9gfYLCq4Xu1PGb+W4u/NW9Ipn8/67J0qN8OAEuKRXI0mESUmvNMe94N9Knh/b6/WwrTUbDZOm4N2fTJAg9P+7wFULk6nwUmj0yxT/GNQIZZFd/dcMt7ZDRoux320X0U1h8PwZwny28070ymveyPjvKfqkUNJeYAxORlHlFDn231wpboz9q3h9MD3cD5owYXVNvqm+wVqr/pdCw0E/S1YpYRcBIa/gUrCssgPbVpGur9eV0S1rWNXOa0xc+7viBIgn7gxl+HyrKOUnDZQ2C26ZL8xo5z8Wpt0BZkQ9AumrRo8ddjvckPvbqLKsBycDw0+HO8PvaAyEYRORicTE+60DNJq0gJapVxhgx3cZYwOaxfsWtyU6+DvLIeDy52MM+cWhcIOlHhOud3rbrd/7Y+qowaaEtKqYbKGykTjKnfbve43aA3bnDYOoL8YwU3V3w8DyoDSAMoOJ63gXGj4YqfR7/f3G+1DXl729+YLuSx9mHFy1hCG7NuusDenXPG3D38djcej8bTEqKT8BeWxAsIH52BPLaQ87vZQY9wYj6u7R0JHX84oFVJvjzxSbTfgF6ju/1ovlGP5HULek8vUrRmHUi0P14ByX8wpa71h54cJJoT4Xa8gKYWC1qmjaMzbGQClNbPlz3t0CHfRLsV5VMKOTs6anmkSVtsfjo67LvM4JkpJmnJehADy63uzKa/7NIPSDSmrgsXicoowVfhwtaN5ktKj/cOh4GxyhErDuS2paP7Q5QqmJxc+bh91Oe72T7Dq5ocl5P6I1kmx6GrNuhL3t4S8G3InU4+nQiqa68pmYySYzPE6cnGnTkXtkFBaDqpEoWfbgmMWNOBCr43WwZaOpBwfYDoIfqZU7AargraCMqXnQcU/b3hkdMBIIyhjr3Da/nHty7+aDKD8+mvInWy9dD1AplF6nRnl/nhyLuPyXGCxj04Og13KtugPNcG2iHUQ9Lc7hdo5+NkIbXkoVMCs7aMDh+Y5UB1uB3Xhlmq1WrPM8/h3dHiKrjSjNIOc5ffXj7yY+zvdoaYf/mKd0OOcF/PMKHL+ucNNTH5uTfM+1xVuboRzINw7q2O6YXBtQwHxfIFbKr387YceJqZlclpqTQvE/Jzxact0Nz7P482z3R43v49XSmnKZ3J/q9vezaRE6Jhwx3VNhm0Lc00xGDgYKwY872ELWgzDI5R4BmY6F4olez6sKZqNKVx1LMsyFUyEt5Zfy3OMFTkiKHLGeLH0V1MZReXKDbm/11OZx/32TutQadRYr65G/bzU7G9Vfq/Gvo9usyw72h6DltLcgn7tuwIIMKO378UiBKb8OIGViMwUSpvxo0FeEENV/pOWNpa34pPpxU5IBmUyKpO6OXUqYBOKXW7/Z0g7a3usHFvZRvmdSPDUmnmfkqbQt/8ZEkyZNT6fmzKCBMpErUzTrcr/K2lJ+2/Ha/E3HTDlQ7l/o/v/Z0ig1JYnVxmLCEl5T+5f6aa7/mfIpL+TkPP8Xnk49+/0R3vnspMwEIXhQ2kpt3IPt6ImKHLRoIIhJBhBFIws3BhNXBojbkxMXLhx6YvbRsJkMgwyPUNl0e8J/px/zqUzJ2lMdihJflOHkpl8bZFFsEB4jshvcjNNX6ey+Z2GlYmoMv1+ZG8q33mHcluD1TGlRtISyX0uoZuOLwMiVLD6uDt2lki+31UQQsnJyxw2v4lI2u/dBIhxXJaikvRvftOZRzJ1BKKMk3KaDu03eyi/5377RiBOWEYk2ecSjt9sZ8QWd/wkRPy2RM7qeRGcEUSHkrOTQUJJhsoQOCWIredcv+nrNUvlEJxjYCslLZLfdIaAIYhRSTcdss3EDhkhwBFDjedkG5l0RtbvjzvAEnZSN1m/v5ZMviXA81BG5Df3eYzkd2oEMojksH4vLELTX5FpDeSgGLh6zvpNOmM1ANIwy0795r/R2yLbGZCJ3hcX+cR5HiNN53wL5JKIqY4nX+I3VYTaxQRIR88LhfKvm4w3Eki5hLMih5LN79lzydQS+blTgnXR6qoCk+8ruwj4MlskmNROYI1EKuqKRYjeyaD696SgwZrRDRV3KCeFJrhApJtdlt/LJ99oTQOXUMy8KlrP7VD67+sBcJPDYG6BxmWLYc/Ryzi4jmIJTXKaDjX52ir9lkQF/oeEHhtk50pnX7bMNvJN56LeRLYZfEhNo29LXXTne93Z22/EA7AZtPSx2TUG/dte79TmzP47wVXjQNuUvxN4eHh4YPkBCQRRm58+7BkAAAAASUVORK5CYII="
const LOGO_SORB = "data:image/png;base64,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"

export default function Login() {
  const [email, setEmail]       = useState("")
  const [password, setPassword] = useState("")
  const [error, setError]       = useState(null)
  const [loading, setLoading]   = useState(false)
  const { login } = useAuth()
  const navigate  = useNavigate()

  usePageTitle("Login");

  const handleLogin = async () => {
    setError(null)
    if (!email || !password) { setError("Remplis tous les champs"); return }
    setLoading(true)
    const data = await authService.login(email, password)
    setLoading(false)
    if (data.success) { login(data.user); navigate("/dashboard") }
    else setError(data.error || "Erreur inconnue")
  }

  return (
    <div style={styles.page}>
      <div style={styles.left}>
        <div style={styles.overlay} />
        <div style={styles.leftContent}>
          <p style={styles.tagline}>Système de gestion<br />des colis et commandes</p>
        </div>
      </div>

      <div style={styles.right}>
        <div style={styles.card}>
          <div style={styles.logos}>
            <img src={LOGO_IUT}  alt="IUT Villetaneuse" style={styles.logoIut} />
            <div style={styles.logoDivider} />
            <img src={LOGO_SORB} alt="Sorbonne Paris Nord" style={styles.logoSorb} />
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
              onKeyDown={e => e.key === "Enter" && handleLogin()}
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

          <p style={styles.registerLink}>
            Pas encore de compte ?{" "}
            <Link to="/register" style={styles.link}>Créer un compte</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: {
    display: "flex",
    minHeight: "100vh",
    fontFamily: "'Segoe UI', system-ui, sans-serif",
  },
  left: {
    flex: 1,
    background: "linear-gradient(160deg, #0d6ebd 0%, #1a9fd4 50%, #0a4f8a 100%)",
    position: "relative",
    display: "flex",
    alignItems: "flex-end",
    padding: "3rem",
    minHeight: "100vh",
  },
  overlay: {
    position: "absolute", inset: 0,
    background: "rgba(5, 40, 80, 0.35)",
  },
  leftContent: {
    position: "relative", zIndex: 1,
  },
  tagline: {
    color: "rgba(255,255,255,0.92)",
    fontSize: "1.5rem",
    fontWeight: 300,
    lineHeight: 1.5,
    margin: 0,
    letterSpacing: "0.01em",
  },
  right: {
    width: "460px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f7f9fc",
    padding: "2rem",
  },
  card: {
    width: "100%",
    maxWidth: "380px",
    background: "#fff",
    borderRadius: "16px",
    padding: "2.5rem 2rem",
    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
  },
  logos: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    marginBottom: "2rem",
  },
  logoIut: {
    height: "52px",
    objectFit: "contain",
  },
  logoDivider: {
    width: "1px",
    height: "40px",
    background: "#dde3ec",
  },
  logoSorb: {
    height: "70px",
    objectFit: "contain",
  },
  title: {
    fontSize: "1.5rem",
    fontWeight: 700,
    color: "#0d2a4a",
    margin: "0 0 0.25rem",
  },
  subtitle: {
    fontSize: "0.875rem",
    color: "#6b7a99",
    margin: "0 0 1.75rem",
  },
  errorBox: {
    background: "#fff3f3",
    border: "1px solid #fbc5c5",
    borderRadius: "8px",
    padding: "0.75rem 1rem",
    fontSize: "0.875rem",
    color: "#c0392b",
    marginBottom: "1.25rem",
    display: "flex",
    alignItems: "center",
  },
  field: {
    marginBottom: "1.25rem",
  },
  label: {
    display: "block",
    fontSize: "0.8125rem",
    fontWeight: 600,
    color: "#3d4f6e",
    marginBottom: "0.4rem",
    letterSpacing: "0.02em",
  },
  input: {
    width: "100%",
    padding: "0.65rem 0.875rem",
    fontSize: "0.9375rem",
    border: "1.5px solid #dde3ec",
    borderRadius: "8px",
    outline: "none",
    boxSizing: "border-box",
    color: "#0d2a4a",
    background: "#fff",
    transition: "border-color 0.15s",
  },
  btn: {
    width: "100%",
    padding: "0.75rem",
    fontSize: "0.9375rem",
    fontWeight: 600,
    background: "linear-gradient(135deg, #1a7fd4, #0d5fa8)",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginTop: "0.5rem",
    letterSpacing: "0.02em",
    transition: "opacity 0.15s",
  },
  registerLink: {
    textAlign: "center",
    fontSize: "0.8125rem",
    color: "#6b7a99",
    marginTop: "1.25rem",
    marginBottom: 0,
  },
  link: {
    color: "#1a7fd4",
    fontWeight: 600,
    textDecoration: "none",
  },
}