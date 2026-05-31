from app.dao.EvenementColisDAO import EvenementColisDAO

class EvenementColisService:
    def __init__(self):
        self.dao = EvenementColisDAO()

    def get_by_colis(self, colis_id):
        return self.dao.get_by_colis(colis_id)

    def get_by_id(self, id_evenement):
        ev = self.dao.get_by_id(id_evenement)
        if not ev:
            raise ValueError(f"Événement {id_evenement} introuvable")
        return ev

    def get_dernier_evenement(self, colis_id):
        return self.dao.get_dernier_evenement(colis_id)

    def get_by_action(self, action):
        ACTIONS_VALIDES = ('scan_reception', 'transfert_iut', 'remise_destinataire', 'incident')
        if action not in ACTIONS_VALIDES:
            raise ValueError(f"Action invalide, valeurs possibles : {ACTIONS_VALIDES}")
        return self.dao.get_by_action(action)

    def get_by_utilisateur(self, utilisateur_id):
        return self.dao.get_by_utilisateur(utilisateur_id)

    def create(self, colis_id, action, utilisateur_id=None, statut_libelle=None,
               commentaire=None, localisation=None, transporteur=None,
               numero_livraison=None, date_expedition=None, date_estimee_arrivee=None):
        if not colis_id or not action:
            raise ValueError("colis_id et action sont requis")
        return self.dao.create(
            colis_id=colis_id,
            action=action,
            utilisateur_id=utilisateur_id,
            statut_libelle=statut_libelle,
            commentaire=commentaire,
            localisation=localisation,
            transporteur=transporteur,
            numero_livraison=numero_livraison,
            date_expedition=date_expedition,
            date_estimee_arrivee=date_estimee_arrivee
        )

    def delete(self, id_evenement):
        self.get_by_id(id_evenement)
        return self.dao.delete(id_evenement)