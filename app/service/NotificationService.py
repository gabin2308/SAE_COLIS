from app.dao.NotificationDAO import NotificationDAO

class NotificationService:

    def __init__(self):
        self.dao = NotificationDAO()

    def get_by_utilisateur(self, id_utilisateur):
        return self.dao.get_by_utilisateur(id_utilisateur)

    def get_non_lues(self, id_utilisateur):
        return self.dao.get_non_lues(id_utilisateur)

    def compter_non_lues(self, id_utilisateur):
        return len(self.dao.get_non_lues(id_utilisateur))

    def envoyer(self, id_utilisateur, message):
        if not message or not message.strip():
            raise ValueError("Le message est requis")
        return self.dao.create(id_utilisateur, message.strip())

    def envoyer_multiple(self, ids_utilisateurs, message):
        if not message or not message.strip():
            raise ValueError("Le message est requis")
        return [self.dao.create(uid, message.strip()) for uid in ids_utilisateurs]

    def marquer_lu(self, id_notification):
        notif = self.dao.get_by_id(id_notification)
        if not notif:
            raise ValueError(f"Notification {id_notification} introuvable")
        return self.dao.marquer_lu(id_notification)

    def marquer_toutes_lues(self, id_utilisateur):
        self.dao.marquer_toutes_lues(id_utilisateur)

    def delete(self, id_notification):
        notif = self.dao.get_by_id(id_notification)
        if not notif:
            raise ValueError(f"Notification {id_notification} introuvable")
        return self.dao.delete(id_notification)

    def delete_toutes(self, id_utilisateur):
        return self.dao.delete_toutes(id_utilisateur)