import { apiFetch } from "./api"

const BASE = "/departement"

export const departementService = {
  // GET /api/departement/
  getAll: async () => {
    return await apiFetch(`${BASE}/`)
  },

  // GET /api/departement/<id>
  getById: async (id_departement) => {
    return await apiFetch(`${BASE}/${id_departement}`)
  },

  // POST /api/departement/
  create: async (data) => {
    return await apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(data)
    })
  },

  // PUT /api/departement/<id>
  update: async (id_departement, data) => {
    return await apiFetch(`${BASE}/${id_departement}`, {
      method: "PUT",
      body: JSON.stringify(data)
    })
  },

  // DELETE /api/departement/<id>
  delete: async (id_departement) => {
    return await apiFetch(`${BASE}/${id_departement}`, {
      method: "DELETE"
    })
  },

  // PATCH /api/departement/<id>/budget
  consommerBudget: async (id_departement, montant) => {
    return await apiFetch(`${BASE}/${id_departement}/budget`, {
      method: "PATCH",
      body: JSON.stringify({ montant })
    })
  }
}