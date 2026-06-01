const BASE = "/api";

export const apiFetch = async (url, options = {}) => {
  const token = localStorage.getItem("token");

  const response = await fetch(`${BASE}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  // 1. Gestion des erreurs HTTP
  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem("token");
      throw new Error("SESSION_EXPIRED");
    }

    // Tente de parser l'erreur en JSON, sinon récupère le texte brut
    const errorData = await response.text();
    let message;
    try {
      message = JSON.parse(errorData).message || errorData;
    } catch {
      message = errorData || `Erreur ${response.status}`;
    }
    throw new Error(message);
  }

  // 2. Retourne null si le contenu est vide, sinon le JSON
  const text = await response.text();
  return text ? JSON.parse(text) : null;
};