class Notification:
    def __init__(self, dico):
        self.id_notification = dico.get('id_notification')
        self.id_utilisateur = dico.get('id_utilisateur')
        self.message_notification = dico.get('message_notification')
        self.date_envoi = dico.get('date_envoi')
        self.lu = bool(dico.get('lu', False))

    def to_dict(self):
        return {
            'id_notification': self.id_notification,
            'id_utilisateur': self.id_utilisateur,
            'message_notification': self.message_notification,
            'date_envoi': str(self.date_envoi) if self.date_envoi else None,
            'lu': self.lu
        }