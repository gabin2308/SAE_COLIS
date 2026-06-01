import { apiFetch } from "./api"

const BASE = "/auth"

export const authService = {
  // 🔐 Connexion
  login: async (email, password) => {
    return await apiFetch(`${BASE}/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    })
  },

  // 🔑 Changer le mot de passe avec le token temporaire
  changePassword: async (newPassword) => {
    // Note : le userId est extrait côté serveur via le jeton JWT
    return await apiFetch(`${BASE}/change-password`, {
      method: "POST",
      body: JSON.stringify({ new_password: newPassword }),
    })
  },

  // 👤 Récupérer le profil de l'utilisateur connecté
  me: async () => {
    return await apiFetch(`${BASE}/me`)
  },

  // 💾 Gestion des jetons
  saveToken: (token) => {
    localStorage.setItem("token", token)
  },

  saveChangeToken: (token, userId) => {
    localStorage.setItem("change_token", token)
    localStorage.setItem("pending_user_id", userId)
  },

  clearAuth: () => {
    localStorage.removeItem("token")
    localStorage.removeItem("change_token")
    localStorage.removeItem("pending_user_id")
  },

  logout: () => {
    authService.clearAuth()
  }
}