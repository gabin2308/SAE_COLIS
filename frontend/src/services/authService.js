import { apiFetch } from "./api"

const BASE = "/auth"

export const authService = {

  // ─────────────────────────────────────────
  // CONNEXION
  // ─────────────────────────────────────────
  login: async (email, password) => {
    return await apiFetch(`${BASE}/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    })
  },

  // ─────────────────────────────────────────
  // CHANGEMENT DE MOT DE PASSE (token temporaire)
  // ─────────────────────────────────────────
  changePassword: async (newPassword) => {
    return await apiFetch(`${BASE}/change-password`, {
      method: "POST",
      body: JSON.stringify({ new_password: newPassword }),
    })
  },

  // ─────────────────────────────────────────
  // PROFIL UTILISATEUR CONNECTÉ
  // ─────────────────────────────────────────
  me: async () => {
    return await apiFetch(`${BASE}/me`)
  },

  // ─────────────────────────────────────────
  // CRÉATION D'UTILISATEUR (admin uniquement)
  // ─────────────────────────────────────────
  register: async ({ full_name, email, password, departement_id }) => {
    return await apiFetch(`${BASE}/register`, {
      method: "POST",
      body: JSON.stringify({ full_name, email, password, departement_id }),
    })
  },

  // ─────────────────────────────────────────
  // DÉCONNEXION
  // ─────────────────────────────────────────
  logout: async () => {
    try {
      await apiFetch(`${BASE}/logout`, { method: "POST" })
    } catch (_) {
      // On nettoie le localStorage même si la requête échoue
    } finally {
      authService.clearAuth()
    }
  },

  // ─────────────────────────────────────────
  // GESTION DES TOKENS LOCAUX
  // ─────────────────────────────────────────

  /** Sauvegarde le token de session normal */
  saveToken: (token) => {
    localStorage.setItem("token", token)
  },

  /** Sauvegarde le token restreint pour le changement de mot de passe forcé */
  saveChangeToken: (token, userId) => {
    localStorage.setItem("change_token", token)
    localStorage.setItem("pending_user_id", String(userId))
  },

  /** Supprime tous les tokens et données de session */
  clearAuth: () => {
    localStorage.removeItem("token")
    localStorage.removeItem("change_token")
    localStorage.removeItem("pending_user_id")
  },

  // ─────────────────────────────────────────
  // HELPERS LOCAUX (lecture sans appel API)
  // ─────────────────────────────────────────

  /** Retourne vrai si un token de session est présent */
  isAuthenticated: () => {
    return !!localStorage.getItem("token")
  },

  /** Retourne vrai si un changement de mot de passe est en attente */
  hasPendingPasswordChange: () => {
    return !!localStorage.getItem("change_token")
  },

  /** Récupère l'id utilisateur en attente de changement de mot de passe */
  getPendingUserId: () => {
    return localStorage.getItem("pending_user_id")
  },
}