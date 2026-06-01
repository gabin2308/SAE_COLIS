const BASE = "/api";

export const apiFetch = async (url, options = {}) => {
  // Détermination automatique du jeton à utiliser
  // Priorité au token de changement s'il existe, sinon le token normal
  const changeToken = localStorage.getItem("change_token");
  const authToken = localStorage.getItem("token");
  const token = changeToken || authToken;

  const response = await fetch(`${BASE}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Nettoyage complet en cas d'expiration
      localStorage.removeItem("token");
      localStorage.removeItem("change_token");
      localStorage.removeItem("pending_user_id");
      throw new Error("SESSION_EXPIRED");
    }

    const errorData = await response.text();
    let message;
    try {
      const parsed = JSON.parse(errorData);
      message = parsed.error || parsed.message || errorData;
    } catch {
      message = errorData || `Erreur ${response.status}`;
    }
    throw new Error(message);
  }

  const text = await response.text();
  return text ? JSON.parse(text) : null;
};