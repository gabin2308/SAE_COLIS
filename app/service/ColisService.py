from datetime import datetime
from app.dao.ColisDAO import ColisDAO

class ColisService:

    def __init__(self):
        self.dao = ColisDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_colis):
        colis = self.dao.get_by_id(id_colis)
        if not colis:
            raise ValueError(f"Colis {id_colis} introuvable")
        return colis

    def get_by_numero_suivi(self, numero_suivi):
        colis = self.dao.get_by_numero_suivi(numero_suivi)
        if not colis:
            raise ValueError(f"Colis avec numéro de suivi '{numero_suivi}' introuvable")
        return colis

    def get_by_destinataire(self, destinataire_id):
        return self.dao.get_by_destinataire(destinataire_id)

    def get_by_bon_commande(self, bon_commande_id):
        return self.dao.get_by_bon_commande(bon_commande_id)

    def get_by_departement(self, departement_id):
        return self.dao.get_by_departement(departement_id)

    def create(self, bon_commande_id, statut_id, numero_suivi=None, code_barres=None,
               destinataire_id=None, commentaire=None, receptionne_par=None):
        if not bon_commande_id or not statut_id:
            raise ValueError("bon_commande_id et statut_id sont requis")
        return self.dao.create(bon_commande_id, statut_id, numero_suivi, code_barres,
                               destinataire_id, commentaire, receptionne_par)

    def update_statut(self, id_colis, statut_id):
        self.get_by_id(id_colis)
        return self.dao.update_statut(id_colis, statut_id)

    def receptionner(self, id_colis, receptionne_par):
        self.get_by_id(id_colis)
        date_reception = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.dao.update_reception(id_colis, receptionne_par, date_reception)

    def retirer(self, id_colis):
        self.get_by_id(id_colis)
        date_retrait = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.dao.update_retrait(id_colis, date_retrait)

    def update(self, id_colis, **kwargs):
        self.get_by_id(id_colis)
        return self.dao.update(id_colis, **kwargs)

    def delete(self, id_colis):
        self.get_by_id(id_colis)
        return self.dao.delete(id_colis)