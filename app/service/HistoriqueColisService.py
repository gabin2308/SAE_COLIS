from app.dao.HistoriqueColisDAO import HistoriqueColisDAO

class HistoriqueColisService:

    def __init__(self):
        self.dao = HistoriqueColisDAO()

    def get_by_colis(self, id_colis):
        return self.dao.get_by_colis(id_colis)

    def get_by_utilisateur(self, utilisateur_id):
        return self.dao.get_by_utilisateur(utilisateur_id)

    def enregistrer(self, id_colis, action, utilisateur_id=None):
        if not id_colis or not action:
            raise ValueError("id_colis et action sont requis")
        return self.dao.create(id_colis, action, utilisateur_id)