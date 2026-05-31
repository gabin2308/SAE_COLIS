const BASE = "/api"

export const apiFetch = async (url, options = {}) => {
  const token = localStorage.getItem("token")

  const res = await fetch(`${BASE}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {}),
      ...options.headers
    }
  })

  return res
}