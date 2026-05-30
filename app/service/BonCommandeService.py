from datetime import datetime
import uuid
from app.dao.BonCommandeDAO import BonCommandeDAO
from app.model.BonCommande import BonCommande

class BonCommandeService:

    def __init__(self):
        self.dao = BonCommandeDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_bon_commande):
        bc = self.dao.get_by_id(id_bon_commande)
        if not bc:
            raise ValueError(f"Bon de commande {id_bon_commande} introuvable")
        return bc

    def get_by_numero(self, numero_commande):
        bc = self.dao.get_by_numero(numero_commande)
        if not bc:
            raise ValueError(f"Bon de commande '{numero_commande}' introuvable")
        return bc

    def get_by_departement(self, departement_id):
        return self.dao.get_by_departement(departement_id)

    def get_by_createur(self, createur_id):
        return self.dao.get_by_createur(createur_id)

    def get_by_statut(self, statut):
        if statut not in BonCommande.STATUTS:
            raise ValueError(f"Statut invalide, valeurs possibles : {BonCommande.STATUTS}")
        return self.dao.get_by_statut(statut)

    def _generer_numero(self):
        date = datetime.now().strftime('%Y%m%d')
        unique = str(uuid.uuid4())[:6].upper()
        return f"BC-{date}-{unique}"

    def create(self, departement_id, fournisseur_id, createur_id, devis_id,
               date_estimee_livraison=None, montant_estime=0, commentaire=None):
        if not all([departement_id, fournisseur_id, createur_id, devis_id]):
            raise ValueError("departement_id, fournisseur_id, createur_id et devis_id sont requis")

        numero_commande = self._generer_numero()
        date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return self.dao.create(
            numero_commande, date_commande, departement_id, fournisseur_id,
            createur_id, devis_id, date_estimee_livraison, montant_estime, commentaire
        )

    def update_statut(self, id_bon_commande, statut):
        if statut not in BonCommande.STATUTS:
            raise ValueError(f"Statut invalide, valeurs possibles : {BonCommande.STATUTS}")
        self.get_by_id(id_bon_commande)
        return self.dao.update_statut(id_bon_commande, statut)

    def update(self, id_bon_commande, date_estimee_livraison=None,
               montant_estime=None, commentaire=None):
        self.get_by_id(id_bon_commande)
        return self.dao.update(id_bon_commande, date_estimee_livraison,
                               montant_estime, commentaire)

    def delete(self, id_bon_commande):
        self.get_by_id(id_bon_commande)
        return self.dao.delete(id_bon_commande)