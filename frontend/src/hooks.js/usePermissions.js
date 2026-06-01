// src/hooks/usePermissions.js
import { useAuth } from "../context/AuthContext";

export const usePermissions = () => {
  const { user } = useAuth();
  
  return {
    isAdmin: user?.role === 'administrateur',
    isAgent: ["administrateur", "postal_iut", "postal_univ"].includes(user?.role),
    isUser: user?.role === 'utilisateur'
  };
};