import { apiFetch } from "./api";

const BASE = "/bon_commande"; // Correspond à l'URL définie dans votre app Flask

export const bonCommandeService = {
  // GET /bon-commande/
  getAll: async () => {
    return await apiFetch(`${BASE}/`);
  },

  // GET /bon-commande/<id_bon_commande>
  getById: async (id_bon_commande) => {
    return await apiFetch(`${BASE}/${id_bon_commande}`);
  },

  // GET /bon-commande/numero/<numero>
  getByNumero: async (numero) => {
    return await apiFetch(`${BASE}/numero/${numero}`);
  },

  // GET /bon-commande/departement/<departement_id>
  getByDepartement: async (departement_id) => {
    return await apiFetch(`${BASE}/departement/${departement_id}`);
  },

  // GET /bon-commande/statut/<statut>
  getByStatut: async (statut) => {
    return await apiFetch(`${BASE}/statut/${statut}`);
  },

  // POST /bon-commande/
  create: async (data) => {
    return await apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  // PATCH /bon-commande/<id_bon_commande>/commentaire
  updateCommentaire: async (id_bon_commande, commentaire) => {
    return await apiFetch(`${BASE}/${id_bon_commande}/commentaire`, {
      method: "PATCH",
      body: JSON.stringify({ commentaire }),
    });
  },

  // PATCH /bon-commande/<id_bon_commande>/valider
  valider: async (id_bon_commande) => {
    return await apiFetch(`${BASE}/${id_bon_commande}/valider`, {
      method: "PATCH",
    });
  },

  // PATCH /bon-commande/<id_bon_commande>/expedier
  expedier: async (id_bon_commande) => {
    return await apiFetch(`${BASE}/${id_bon_commande}/expedier`, {
      method: "PATCH",
    });
  },

  // PATCH /bon-commande/<id_bon_commande>/confirmer
  confirmerLivraison: async (id_bon_commande) => {
    return await apiFetch(`${BASE}/${id_bon_commande}/confirmer`, {
      method: "PATCH",
    });
  },

  // PATCH /bon-commande/<id_bon_commande>/annuler
  annuler: async (id_bon_commande) => {
    return await apiFetch(`${BASE}/${id_bon_commande}/annuler`, {
      method: "PATCH",
    });
  },

  // DELETE /bon-commande/<id_bon_commande>
  delete: async (id_bon_commande) => {
    return await apiFetch(`${BASE}/${id_bon_commande}`, {
      method: "DELETE",
    });
  },
};