
class Fournisseur:
    def __init__(self, dico):
        self.id_fournisseur = dico.get('id_fournisseur')
        self.nom = dico.get('nom')
        self.contact_nom = dico.get('contact_nom')
        self.contact_email = dico.get('contact_email')
        self.contact_telephone = dico.get('contact_telephone')

    def to_dict(self):
        return {
            'id_fournisseur': self.id_fournisseur,
            'nom': self.nom,
            'contact_nom': self.contact_nom,
            'contact_email': self.contact_email,
            'contact_telephone': self.contact_telephone
        }