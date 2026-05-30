from app.dao.DemandeAchatDAO import DemandeAchatDAO
from app.model.DemandeAchat import DemandeAchat
from app.service.NotificationService import NotificationService
from app.dao.UserDAO import UtilisateurDAO
from app.service.DepartementService import DepartementService


class DemandeAchatService:

    def __init__(self):
        self.dao = DemandeAchatDAO()
        self.notif = NotificationService()
        self.user_dao = UtilisateurDAO()
        self.dep_service = DepartementService()  

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_demande):
        demande = self.dao.get_by_id(id_demande)
        if not demande:
            raise ValueError(f"Demande {id_demande} introuvable")
        return demande

    def get_by_demandeur(self, demandeur_id):
        return self.dao.get_by_demandeur(demandeur_id)

    def get_by_departement(self, departement_id):
        return self.dao.get_by_departement(departement_id)

    def get_en_attente_departement(self, departement_id):
        return self.dao.get_en_attente_departement(departement_id)

    def create(self, objet, demandeur_id, departement_id,
               description=None, montant_estime=None):
        if not objet or not objet.strip():
            raise ValueError("L'objet est requis")
        if not demandeur_id or not departement_id:
            raise ValueError("demandeur_id et departement_id sont requis")

        demande = self.dao.create(objet.strip(), demandeur_id,
                                  departement_id, description, montant_estime)

        # Notifie les responsables du département
        responsables = self.user_dao.get_by_role('directeur')
        for r in responsables:
            if r.departement_id == departement_id:
                self.notif.envoyer(
                    r.id_utilisateur,
                    f"Nouvelle demande d'achat : '{objet}' en attente de validation."
                )

        return demande

    def approuver(self, id_demande, commentaire=None):
        demande = self.get_by_id(id_demande)
        if demande.statut != 'en_attente':
            raise ValueError("Seules les demandes en attente peuvent être approuvées")

        # Consomme le budget si un montant est estimé
        if demande.montant_estime and demande.montant_estime > 0:
            self.dep_service.consommer_budget(
                demande.departement_id,
                demande.montant_estime
            )

        updated = self.dao.update_statut(id_demande, 'approuvee', commentaire)

        self.notif.envoyer(
            demande.demandeur_id,
            f"Votre demande '{demande.objet}' a été approuvée."
        )
        return updated

    def refuser(self, id_demande, commentaire=None):
        demande = self.get_by_id(id_demande)
        if demande.statut != 'en_attente':
            raise ValueError("Seules les demandes en attente peuvent être refusées")

        updated = self.dao.update_statut(id_demande, 'refusee', commentaire)

        # Notifie le demandeur
        self.notif.envoyer(
            demande.demandeur_id,
            f"Votre demande '{demande.objet}' a été refusée."
            + (f" Motif : {commentaire}" if commentaire else "")
        )
        return updated

    def delete(self, id_demande):
        demande = self.get_by_id(id_demande)
        if demande.statut != 'en_attente':
            raise ValueError("Seules les demandes en attente peuvent être supprimées")
        return self.dao.delete(id_demande)