const BASE = "/api/users";

export const adminUserService = {
  
  // GET all users
  getAll: async () => {
    const res = await fetch(`${BASE}/`, {
      method: "GET",
      credentials: "include",
    });

    if (!res.ok) {
      return { error: "Erreur lors du chargement des utilisateurs" };
    }

    return await res.json();
  },

  // GET user by id
  getById: async (id) => {
    const res = await fetch(`${BASE}/${id}`, {
      method: "GET",
      credentials: "include",
    });

    if (res.status === 404) {
      return { error: "Utilisateur introuvable" };
    }

    return await res.json();
  },

  // SEARCH users
  search: async (query) => {
    const res = await fetch(`${BASE}/search?q=${encodeURIComponent(query)}`, {
      method: "GET",
      credentials: "include",
    });

    if (!res.ok) {
      return { error: "Erreur recherche" };
    }

    return await res.json();
  },

  // CREATE user (admin only)
  create: async (userData) => {
    const res = await fetch(`${BASE}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(userData),
    });

    const data = await res.json();

    if (res.status === 409) {
      return { error: data.error };
    }

    if (!res.ok) {
      return { error: data.error || "Erreur création utilisateur" };
    }

    return data;
  },

  // UPDATE user
  update: async (id, userData) => {
    const res = await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(userData),
    });

    const data = await res.json();

    if (res.status === 404) {
      return { error: "Utilisateur introuvable" };
    }

    if (!res.ok) {
      return { error: data.error || "Erreur update" };
    }

    return data;
  },

  // UPDATE password
  updatePassword: async (id, password) => {
    const res = await fetch(`${BASE}/${id}/password`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ password }),
    });

    const data = await res.json();

    if (res.status === 400) {
      return { error: data.error };
    }

    if (!res.ok) {
      return { error: "Erreur update password" };
    }

    return data;
  },

  // DELETE user
  delete: async (id) => {
    const res = await fetch(`${BASE}/${id}`, {
      method: "DELETE",
      credentials: "include",
    });

    const data = await res.json();

    if (res.status === 403) {
      return { error: data.error };
    }

    if (!res.ok) {
      return { error: data.error || "Erreur suppression" };
    }

    return data;
  },
};