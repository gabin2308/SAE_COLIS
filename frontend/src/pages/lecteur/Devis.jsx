import React, { useState, useEffect } from 'react';
import { devisService } from '../../services/devisService'; // Ajustez le chemin

const DevisManager = () => {
  const [devisList, setDevisList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Charger les devis au montage du composant
  useEffect(() => {
    loadDevis();
  }, []);

  const loadDevis = async () => {
    try {
      setLoading(true);
      const data = await devisService.getAll();
      setDevisList(data);
    } catch (err) {
      setError("Erreur lors du chargement des devis");
    } finally {
      setLoading(false);
    }
  };

  const handleAccepter = async (id) => {
    try {
      await devisService.accepter(id);
      // Recharger la liste après modification
      loadDevis();
    } catch (err) {
      alert("Impossible d'accepter ce devis");
    }
  };

  if (loading) return <div>Chargement en cours...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Gestion des Devis</h1>
      <ul>
        {devisList.map((devis) => (
          <li key={devis.id_devis}>
            {devis.objet} - {devis.montant_estime}€
            <button onClick={() => handleAccepter(devis.id_devis)}>
              Accepter
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DevisManager;