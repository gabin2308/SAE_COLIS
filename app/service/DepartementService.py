from app.dao.DepartementDAO import DepartementDAO

class DepartementService:

    def __init__(self):
        self.dao = DepartementDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_departement):
        dep = self.dao.get_by_id(id_departement)
        if not dep:
            raise ValueError(f"Département {id_departement} introuvable")
        return dep

    def create(self, nom, telephone=None, budget_total=0):
        if not nom or not nom.strip():
            raise ValueError("Le nom est requis")
        if self.dao.get_by_nom(nom):
            raise ValueError(f"Le département '{nom}' existe déjà")
        return self.dao.create(nom.strip(), telephone, budget_total)

    def update(self, id_departement, nom=None, telephone=None, budget_total=None):
        self.get_by_id(id_departement)  # vérifie existence
        if nom:
            existing = self.dao.get_by_nom(nom)
            if existing and existing.id_departement != id_departement:
                raise ValueError(f"Le département '{nom}' existe déjà")
        return self.dao.update(id_departement, nom, telephone, budget_total)

    def consommer_budget(self, id_departement, montant):
            dep = self.get_by_id(id_departement)
            if montant <= 0:
                raise ValueError("Le montant doit être positif")
            
            budget_restant = dep.budget_total - dep.budget_utilise
            
            if budget_restant < montant:
                raise ValueError(f"Budget insuffisant (restant: {budget_restant}€)")
                
            return self.dao.update_budget_utilise(id_departement, montant)
    
    def delete(self, id_departement):
        self.get_by_id(id_departement)  # vérifie existence
        return self.dao.delete(id_departement)