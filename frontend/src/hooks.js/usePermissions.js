import { useAuth } from "../context/AuthContext";

export const usePermissions = () => {
  const { user } = useAuth();
  
  return {
    isAdmin: user?.role === 'administrateur',
    // Utilisation des noms exacts insérés dans la base de données
    isAgent: ["administrateur", "agent_postal_iut", "agent_postal_universite"].includes(user?.role),
    isResponsableFinancier: user?.role === 'responsable_financier',
    isDirecteur: user?.role === 'directeur',
    isResponsableDept: user?.role === 'responsable_departement',
    isLecteur: user?.role === 'lecteur'
  };
};