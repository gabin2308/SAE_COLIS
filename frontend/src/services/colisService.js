const BASE = "/api/colis";

export const colisService = {

  getAll: async () => {
    const res = await fetch(`${BASE}/`, { credentials: "include" })
    if (!res.ok) return null
    return res.json()
  },

  getMesColis: async () => {
    const res = await fetch(`${BASE}/mes-colis`, { credentials: "include" })
    if (!res.ok) return null
    return res.json()
  },

  getById: async (id) => {
    const res = await fetch(`${BASE}/${id}`, { credentials: "include" })
    if (!res.ok) return null
    return res.json()
  },

  create: async (data) => {
    const res = await fetch(`${BASE}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(data),
    })
    if (!res.ok) return null
    return res.json()
  },

  updateStatut: async (id, statut_id) => {
    const res = await fetch(`${BASE}/${id}/statut`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ statut_id }),
    })
    if (!res.ok) return null
    return res.json()
  },

  receptionner: async (id) => {
    const res = await fetch(`${BASE}/${id}/receptionner`, {
      method: "PATCH",
      credentials: "include",
    })
    if (!res.ok) return null
    return res.json()
  },

  retirer: async (id) => {
    const res = await fetch(`${BASE}/${id}/retirer`, {
      method: "PATCH",
      credentials: "include",
    })
    if (!res.ok) return null
    return res.json()
  },

  delete: async (id) => {
    const res = await fetch(`${BASE}/${id}`, {
      method: "DELETE",
      credentials: "include",
    })
    if (!res.ok) return null
    return res.json()
  },
}