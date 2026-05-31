class Departement:
    def __init__(self, dico):
        self.id_departement = dico.get('id_departement')
        self.nom            = dico.get('nom')
        self.telephone      = dico.get('telephone')
        self.email          = dico.get('email')
        self.budget_total   = dico.get('budget_total', 0)
        self.budget_utilise = dico.get('budget_utilise', 0)
        self.adresse_id     = dico.get('adresse_id')
        # Jointure
        self.adresse_ville  = dico.get('adresse_ville')
 
    def to_dict(self):
        return {
            'id_departement': self.id_departement,
            'nom':            self.nom,
            'telephone':      self.telephone,
            'email':          self.email,
            'budget_total':   self.budget_total,
            'budget_utilise': self.budget_utilise,
            'adresse_id':     self.adresse_id,
            'adresse_ville':  self.adresse_ville,
        }
