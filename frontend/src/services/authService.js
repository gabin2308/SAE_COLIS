const BASE = "/api/auth";

export const authService = {

  login: async (email, password) => {
    const res = await fetch(`${BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password })
    });
    if (res.status === 429) return { error: "Trop de tentatives, réessaye plus tard.", status: 429 };
    if (res.status === 401) return { error: "Email ou mot de passe incorrect" };
    if (!res.ok) return { error: "Erreur serveur" };
    // Flask retourne {message: "Connexion réussie"}, on fetch /me pour avoir les infos user
    const me = await authService.me();
    if (me.id) return { success: true, user: me };
    return { error: "Erreur lors de la récupération du profil" };
  },

  logout: async () => {
    const res = await fetch(`${BASE}/logout`, { method: "POST", credentials: "include" });
    return res.json();
  },

  me: async () => {
    const res = await fetch(`${BASE}/me`, { credentials: "include" });
    if (!res.ok) return {};
    return res.json();
  },

  register: async (full_name, email, password, role_id, departement_id) => {
    const res = await fetch(`${BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ full_name, email, password, role_id, departement_id })
    });
    if (res.status === 429) return { error: "Trop de tentatives, réessaye plus tard." };
    return res.json();
  }
};