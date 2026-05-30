from datetime import datetime
from app.dao.DevisDAO import DevisDAO
from app.model.Devis import Devis

class DevisService:

    def __init__(self):
        self.dao = DevisDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_devis):
        devis = self.dao.get_by_id(id_devis)
        if not devis:
            raise ValueError(f"Devis {id_devis} introuvable")
        return devis

    def get_by_fournisseur(self, fournisseur_id):
        return self.dao.get_by_fournisseur(fournisseur_id)

    def get_by_createur(self, createur_id):
        return self.dao.get_by_createur(createur_id)

    def get_by_statut(self, statut):
        if statut not in Devis.STATUTS:
            raise ValueError(f"Statut invalide, valeurs possibles : {Devis.STATUTS}")
        return self.dao.get_by_statut(statut)

    def create(self, fournisseur_id, createur_id, objet=None,
               montant_estime=None, fichier_pdf=None):
        if not fournisseur_id or not createur_id:
            raise ValueError("fournisseur_id et createur_id sont requis")
        date_demande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.dao.create(date_demande, fournisseur_id, createur_id,
                               objet, montant_estime, fichier_pdf)

    def accepter(self, id_devis):
        self.get_by_id(id_devis)
        return self.dao.update_statut(id_devis, 'accepte')

    def refuser(self, id_devis):
        self.get_by_id(id_devis)
        return self.dao.update_statut(id_devis, 'refuse')

    def update(self, id_devis, objet=None, montant_estime=None,
               fichier_pdf=None, fournisseur_id=None):
        self.get_by_id(id_devis)
        return self.dao.update(id_devis, objet, montant_estime, fichier_pdf, fournisseur_id)

    def delete(self, id_devis):
        self.get_by_id(id_devis)
        return self.dao.delete(id_devis)