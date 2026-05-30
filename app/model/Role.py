class Role:
    def __init__(self, dico):
        self.id_role = dico.get('id_role')
        self.libelle = dico.get('libelle')

    def to_dict(self):
        return {
            'id_role': self.id_role,
            'libelle': self.libelle
        }