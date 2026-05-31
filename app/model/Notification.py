class Notification:
    def __init__(self, dico):
        self.id_notification = dico.get('id_notification')
        self.id_utilisateur  = dico.get('id_utilisateur')
        self.message         = dico.get('message')
        self.date_envoi      = dico.get('date_envoi')
        self.lu              = dico.get('lu', 0)
        self.type            = dico.get('type')
        self.reference_id    = dico.get('reference_id')
        # Jointure
        self.utilisateur_nom = dico.get('utilisateur_nom')
 
    def to_dict(self):
        return {
            'id_notification': self.id_notification,
            'id_utilisateur':  self.id_utilisateur,
            'utilisateur_nom': self.utilisateur_nom,
            'message':         self.message,
            'date_envoi':      self.date_envoi,
            'lu':              self.lu,
            'type':            self.type,
            'reference_id':    self.reference_id,
        }
