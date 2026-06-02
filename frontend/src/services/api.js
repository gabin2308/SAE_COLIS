const BASE = "/api";

export const apiFetch = async (url, options = {}, isBlob = false) => {
  const changeToken = localStorage.getItem("change_token");
  const authToken = localStorage.getItem("token");
  const token = changeToken || authToken;

  const response = await fetch(`${BASE}${url}`, {
    ...options,
    headers: {
      // On ne force le Content-Type que si ce n'est pas un blob (pour éviter les conflits)
      ...(!isBlob && { "Content-Type": "application/json" }),
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
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

  // Si c'est un blob, on retourne le blob sans tenter de parser
  if (isBlob) {
    return await response.blob();
  }

  const text = await response.text();
  return text ? JSON.parse(text) : null;
};