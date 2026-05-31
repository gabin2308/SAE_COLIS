import { apiFetch } from "./api"

const BASE = "/demande_achat"

export const demandeAchatService = {

  // 🔍 Toutes les demandes
  getAll: async () => {
    const res = await apiFetch(`${BASE}/`)
    if (!res.ok) throw new Error("Erreur chargement demandes")
    return res.json()
  },

  // 🔍 Une demande par ID
  getById: async (id) => {
    const res = await apiFetch(`${BASE}/${id}`)
    if (!res.ok) throw new Error("Demande introuvable")
    return res.json()
  },

  // 👤 Mes demandes (user connecté)
  getMesDemandes: async () => {
    const res = await apiFetch(`${BASE}/mes-demandes`)
    if (!res.ok) throw new Error("Erreur mes demandes")
    return res.json()
  },

  // 🏢 Par département
  getByDepartement: async (departementId) => {
    const res = await apiFetch(`${BASE}/departement/${departementId}`)
    if (!res.ok) throw new Error("Erreur département")
    return res.json()
  },

  // ⏳ En attente par département
  getEnAttente: async (departementId) => {
    const res = await apiFetch(`${BASE}/departement/${departementId}/en-attente`)
    if (!res.ok) throw new Error("Erreur demandes en attente")
    return res.json()
  },

  // ➕ Créer une demande
  create: async (data) => {
    const res = await apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(data)
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.error || "Erreur création demande")
    }

    return res.json()
  },

  // ✅ Approuver
  approuver: async (id, commentaire = "") => {
    const res = await apiFetch(`${BASE}/${id}/approuver`, {
      method: "PATCH",
      body: JSON.stringify({ commentaire })
    })

    if (!res.ok) throw new Error("Erreur approbation")
    return res.json()
  },

  // ❌ Refuser
  refuser: async (id, commentaire = "") => {
    const res = await apiFetch(`${BASE}/${id}/refuser`, {
      method: "PATCH",
      body: JSON.stringify({ commentaire })
    })

    if (!res.ok) throw new Error("Erreur refus")
    return res.json()
  },

  // 🗑 supprimer
  delete: async (id) => {
    const res = await apiFetch(`${BASE}/${id}`, {
      method: "DELETE"
    })

    if (!res.ok) throw new Error("Erreur suppression")
    return res.json()
  }
}