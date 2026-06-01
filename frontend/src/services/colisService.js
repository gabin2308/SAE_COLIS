import { apiFetch } from "./api"

const BASE = "/colis"

export const colisService = {

  // 🔍 Tous les colis (Admin, Agent postal)
  getAll: async () => {
    return await apiFetch(`${BASE}/`)
  },

  // 🔍 Un colis par ID
  getById: async (id_colis) => {
    return await apiFetch(`${BASE}/${id_colis}`)
  },

  // 🔍 Un colis par numéro de suivi transporteur
  getByNumeroSuivi: async (numero_suivi) => {
    return await apiFetch(`${BASE}/suivi/${numero_suivi}`)
  },

  // 👤 Mes colis (user connecté)
  getMesColis: async () => {
    return await apiFetch(`${BASE}/mes-colis`)
  },

  // 📄 Par bon de commande
  getByBonCommande: async (bon_commande_id) => {
    return await apiFetch(`${BASE}/bon-commande/${bon_commande_id}`)
  },

  // ➕ Créer un colis
  create: async (data) => {
    return await apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(data)
    })
  },

  // 📥 Réceptionner le colis (Scan initial à l'université)
  receptionner: async (id_colis) => {
    return await apiFetch(`${BASE}/${id_colis}/receptionner`, {
      method: "PATCH"
    })
  },

  // 🚚 Transférer à l'IUT
  transfererIut: async (id_colis) => {
    return await apiFetch(`${BASE}/${id_colis}/transferer`, {
      method: "PATCH"
    })
  },

  // 🤝 Retirer le colis (Remise en main propre au destinataire)
  retirer: async (id_colis) => {
    return await apiFetch(`${BASE}/${id_colis}/retirer`, {
      method: "PATCH"
    })
  },

  // ⚠️ Signaler un incident
  signalerIncident: async (id_colis, commentaire = "") => {
    return await apiFetch(`${BASE}/${id_colis}/incident`, {
      method: "PATCH",
      body: JSON.stringify({ commentaire })
    })
  },

  // 📝 Mettre à jour les informations du colis
  update: async (id_colis, data) => {
    return await apiFetch(`${BASE}/${id_colis}`, {
      method: "PUT",
      body: JSON.stringify(data)
    })
  },

  // 🗑 Supprimer définitivement un colis
  delete: async (id_colis) => {
    return await apiFetch(`${BASE}/${id_colis}`, {
      method: "DELETE"
    })
  },

  // 📷 Traiter le scan d'un QR code payload
  scanQR: async (qr_payload) => {
    return await apiFetch(`${BASE}/scan/${encodeURIComponent(qr_payload)}`)
  }
}