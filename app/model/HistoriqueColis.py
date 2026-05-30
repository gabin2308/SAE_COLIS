class HistoriqueColis:
    def __init__(self, dico):
        self.id = dico.get('id')
        self.id_colis = dico.get('id_colis')
        self.action = dico.get('action')
        self.date_action = dico.get('date_action')
        self.utilisateur = dico.get('utilisateur', 'postal_iut')

    def to_dict(self):
        return {
            'id': self.id,
            'id_colis': self.id_colis,
            'action': self.action,
            'date_action': str(self.date_action) if self.date_action else None,
            'utilisateur': self.utilisateur
        }
