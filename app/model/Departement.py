

class Departement:
    def __init__(self, dico):
        self.id_departement = dico.get('id_departement')
        self.nom = dico.get('nom')
        self.telephone = dico.get('telephone')
        self.budget_total = dico.get('budget_total', 0)
        self.budget_utilise = dico.get('budget_utilise', 0)

    @property
    def budget_restant(self):
        return self.budget_total - self.budget_utilise

    def to_dict(self):
        return {
            'id_departement': self.id_departement,
            'nom': self.nom,
            'telephone': self.telephone,
            'budget_total': self.budget_total,
            'budget_utilise': self.budget_utilise,
            'budget_restant': self.budget_restant
        }
