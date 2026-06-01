import { apiFetch } from "./api"

const BASE = "/auth"

export const authService = {
  // 🔐 Connexion
  login: async (email, password) => {
    // apiFetch renvoie directement les données JSON (ex: { access_token: "..." })
    return await apiFetch(`${BASE}/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    })
  },

  // 👤 Récupérer le profil de l'utilisateur connecté
  me: async () => {
    return await apiFetch(`${BASE}/me`)
  },

  // 💾 Gestion du token dans le localStorage
  saveToken: (token) => {
    localStorage.setItem("token", token)
  },

  getToken: () => {
    return localStorage.getItem("token")
  },

  logout: () => {
    localStorage.removeItem("token")
  }
}