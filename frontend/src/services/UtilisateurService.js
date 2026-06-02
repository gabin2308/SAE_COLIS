import { apiFetch } from "./api"; // Importez votre fonction

export const userService = {
  getAll: () => apiFetch("/users/"),
  
  getById: (id) => apiFetch(`/users/${id}`),
  
  update: (id, userData) => apiFetch(`/users/${id}`, {
    method: "PUT",
    body: JSON.stringify(userData)
  }),

  delete: (id) => apiFetch(`/users/${id}`, {
    method: "DELETE"
  })
};