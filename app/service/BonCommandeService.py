from datetime import datetime
import uuid
from app.dao.BonCommandeDAO import BonCommandeDAO

STATUTS_VALIDES = ('en_preparation', 'valide_finance', 'expedie', 'livre_confirme', 'annule')

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

    def get_by_fournisseur(self, fournisseur_id):
        return self.dao.get_by_fournisseur(fournisseur_id)

    def get_by_statut(self, statut):
        if statut not in STATUTS_VALIDES:
            raise ValueError(f"Statut invalide, valeurs possibles : {STATUTS_VALIDES}")
        return self.dao.get_by_statut(statut)

    def _generer_numero(self):
        date = datetime.now().strftime('%Y%m%d')
        unique = str(uuid.uuid4())[:6].upper()
        return f"BC-{date}-{unique}"

    def create(self, departement_id, fournisseur_id, createur_id, devis_id,
               date_estimee_livraison=None, montant_estime=0, commentaire=None):
        existing = self.dao.get_by_devis(devis_id)
        if existing:
            raise ValueError(f"Un bon de commande existe déjà pour le devis {devis_id}")
        
        if not all([departement_id, fournisseur_id, createur_id, devis_id]):
            raise ValueError("departement_id, fournisseur_id, createur_id et devis_id sont requis")
        numero_commande = self._generer_numero()
        return self.dao.create(                     # ✅ signature alignée avec le DAO
            numero_commande=numero_commande,
            departement_id=departement_id,
            fournisseur_id=fournisseur_id,
            createur_id=createur_id,
            devis_id=devis_id,
            montant_estime=montant_estime,
            date_estimee_livraison=date_estimee_livraison,
            commentaire=commentaire
        )

    def valider(self, id_bon_commande):             # ✅ méthodes métier du DAO
        self.get_by_id(id_bon_commande)
        return self.dao.valider(id_bon_commande)

    def expedier(self, id_bon_commande):
        self.get_by_id(id_bon_commande)
        return self.dao.expedier(id_bon_commande)

    def confirmer_livraison(self, id_bon_commande):
        self.get_by_id(id_bon_commande)
        return self.dao.confirmer_livraison(id_bon_commande)

    def annuler(self, id_bon_commande):
        self.get_by_id(id_bon_commande)
        return self.dao.annuler(id_bon_commande)

    def update_commentaire(self, id_bon_commande, commentaire):
        self.get_by_id(id_bon_commande)
        return self.dao.update_commentaire(id_bon_commande, commentaire)

    def delete(self, id_bon_commande):
        self.get_by_id(id_bon_commande)
        return self.dao.delete(id_bon_commande)