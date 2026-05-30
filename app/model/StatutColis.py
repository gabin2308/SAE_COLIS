class StatutColis:
    def __init__(self, dico):
        self.id_statut = dico.get('id_statut')
        self.libelle = dico.get('libelle')

    def to_dict(self):
        return {
            'id_statut': self.id_statut,
            'libelle': self.libelle
        }