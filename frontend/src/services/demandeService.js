import { apiFetch } from "./api"

const BASE = "/demande_achat"

export const demandeService = {

  // 🔍 Toutes les demandes (Admin)
  getAll: async () => {
    return await apiFetch(`${BASE}/`)
  },

  // 🔍 Une demande par ID
  getById: async (id) => {
    return await apiFetch(`${BASE}/${id}`)
  },

  // 👤 Mes demandes (user connecté)
  getMesDemandes: async () => {
    return await apiFetch(`${BASE}/mes-demandes`)
  },

  // 🏢 Par département
  getByDepartement: async (departementId) => {
    return await apiFetch(`${BASE}/departement/${departementId}`)
  },

  // ⏳ En attente par département
  getEnAttente: async (departementId) => {
    return await apiFetch(`${BASE}/departement/${departementId}/en-attente`)
  },

  // ➕ Créer une demande
  create: async (data) => {
    return await apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(data)
    })
  },

  // ✅ Approuver une demande
  approuver: async (id, commentaire = "") => {
    return await apiFetch(`${BASE}/${id}/approuver`, {
      method: "PATCH",
      body: JSON.stringify({ commentaire })
    })
  },

  // ❌ Refuser une demande
  refuser: async (id, commentaire = "") => {
    return await apiFetch(`${BASE}/${id}/refuser`, {
      method: "PATCH",
      body: JSON.stringify({ commentaire })
    })
  },

  // 🗑 Supprimer une demande
  delete: async (id) => {
    return await apiFetch(`${BASE}/${id}`, {
      method: "DELETE"
    })
  }
}