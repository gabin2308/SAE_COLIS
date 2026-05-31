import { apiFetch } from "./api"

export const authService = {
  login: async (email, password) => {
    const res = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    })
    const data = await res.json()
    if(!res.ok){
      return { succes: false , error : data.error || "Erreur login"}
    }

    if(data.token){
      localStorage.setItem("token", data.token)
    }
    return {success: true, user: data.user, token: data.token}

    if (res.status === 429) return { error: "Trop de tentatives. Réessayez plus tard." }
    return res.json()
  },

  logout: () => localStorage.removeItem("token"),

  me: async () => {
    const res = await apiFetch("/auth/me")
    if (!res.ok) return null
    return res.json()
  },

  register: async (full_name, email, password, role_id, departement_id) => {
  const res = await apiFetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      full_name,
      email,
      password,
      role_id,
      departement_id
    })
  });

  if (res.status === 429) {
    return { error: "Trop de tentatives, réessaye plus tard." };
  }

  return res.json();
},

  saveToken: (token) => localStorage.setItem("token", token),
  getToken: () => localStorage.getItem("token"),
  isConnected: () => !!localStorage.getItem("token")
}