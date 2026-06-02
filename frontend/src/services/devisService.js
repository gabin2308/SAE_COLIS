import { apiFetch } from "./api";

const BASE = "/devis"; 

export const devisService = {
  // GET /devis/
  getAll: async () => {
    return await apiFetch(`${BASE}/`);
  },

  // GET /devis/<id_devis>
  getById: async (id_devis) => {
    return await apiFetch(`${BASE}/${id_devis}`);
  },

  // GET /devis/fournisseur/<fournisseur_id>
  getByFournisseur: async (fournisseur_id) => {
    return await apiFetch(`${BASE}/fournisseur/${fournisseur_id}`);
  },

  // GET /devis/statut/<statut>
  getByStatut: async (statut) => {
    return await apiFetch(`${BASE}/statut/${statut}`);
  },

  // POST /devis/
  create: async (data) => {
    return await apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  // PUT /devis/<id_devis>
  update: async (id_devis, data) => {
    return await apiFetch(`${BASE}/${id_devis}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  // PATCH /devis/<id_devis>/accepter
  accepter: async (id_devis) => {
    return await apiFetch(`${BASE}/${id_devis}/accepter`, {
      method: "PATCH",
    });
  },

  // PATCH /devis/<id_devis>/refuser
  refuser: async (id_devis) => {
    return await apiFetch(`${BASE}/${id_devis}/refuser`, {
      method: "PATCH",
    });
  },

  // DELETE /devis/<id_devis>
  delete: async (id_devis) => {
    return await apiFetch(`${BASE}/${id_devis}`, {
      method: "DELETE",
    });
  },

  telechargerPdf: async (id_devis) => {
    // On appelle apiFetch avec le 3ème argument 'true' pour le blob
    const blob = await apiFetch(`${BASE}/${id_devis}/pdf`, { method: 'GET' }, true);
    
    // Création du lien de téléchargement
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `devis_${id_devis}.pdf`;
    document.body.appendChild(a);
    a.click();
    
    // Nettoyage
    a.remove();
    window.URL.revokeObjectURL(url);
  }
};