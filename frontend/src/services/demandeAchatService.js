const BASE = "/api/demande_achat"

export const demandeAchatService = {

  getMesDemandes: async () => {
    const res = await fetch(`${BASE}/mes-demandes`, {
      credentials: "include"
    })
    if (!res.ok) return { error: "Erreur chargement demandes" }
    return await res.json()
  },

  create: async (data) => {
    const res = await fetch(`${BASE}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(data)
    })
    const json = await res.json()
    if (!res.ok) return { error: json.error || "Erreur création" }
    return json
  },

  delete: async (id) => {
    const res = await fetch(`${BASE}/${id}`, {
      method: "DELETE",
      credentials: "include"
    })
    const json = await res.json()
    if (!res.ok) return { error: json.error || "Erreur suppression" }
    return json
  },

}