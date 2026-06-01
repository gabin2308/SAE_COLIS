import { apiFetch } from "./api"

// Comme ton backend enregistre ce contrôleur avec le prefixe "/api/notification",
// le BASE ici doit être "/notification" pour que apiFetch concatène en "/api/notification"
const BASE = "/notification"

export const notificationService = {
  // 🔔 Récupérer toutes les notifications (GET /api/notification/)
  getMesNotifications: async () => {
    return await apiFetch(`${BASE}/`)
  },

  // ✉️ Uniquement les non-lues (GET /api/notification/non-lues)
  getNonLues: async () => {
    return await apiFetch(`${BASE}/non-lues`)
  },

  // 🔢 Compter les non-lues (GET /api/notification/count)
  compterNonLues: async () => {
    return await apiFetch(`${BASE}/count`)
  },

  // 📖 Marquer une spécifique comme lue (PATCH /api/notification/<id>/lire)
  marquerLu: async (id_notification) => {
    return await apiFetch(`${BASE}/${id_notification}/lire`, {
      method: "PATCH"
    })
  },

  // ✔️ Tout marquer comme lu (PATCH /api/notification/lire-toutes)
  marquerToutesLues: async () => {
    return await apiFetch(`${BASE}/lire-toutes`, {
      method: "PATCH"
    })
  },

  // 🗑 Supprimer par ID (DELETE /api/notification/<id>)
  delete: async (id_notification) => {
    return await apiFetch(`${BASE}/${id_notification}`, {
      method: "DELETE"
    })
  },

  // 🔥 Supprimer tout l'historique (DELETE /api/notification/tout-supprimer)
  deleteToutes: async () => {
    return await apiFetch(`${BASE}/tout-supprimer`, {
      method: "DELETE"
    })
  },

  // ✉️ Envoyer une notification (POST /api/notification/envoyer)
  envoyer: async (data) => {
    return await apiFetch(`${BASE}/envoyer`, {
      method: "POST",
      body: JSON.stringify(data)
    })
  }
}