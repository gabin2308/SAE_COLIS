from app.dao.FournisseurDAO import FournisseurDAO

class FournisseurService:

    def __init__(self):
        self.dao = FournisseurDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_fournisseur):
        f = self.dao.get_by_id(id_fournisseur)
        if not f:
            raise ValueError(f"Fournisseur {id_fournisseur} introuvable")
        return f

    def create(self, nom, contact_nom=None, contact_email=None, contact_telephone=None):
        if not nom or not nom.strip():
            raise ValueError("Le nom est requis")
        if self.dao.get_by_nom(nom):
            raise ValueError(f"Le fournisseur '{nom}' existe déjà")
        return self.dao.create(nom.strip(), contact_nom, contact_email, contact_telephone)

    def update(self, id_fournisseur, nom=None, contact_nom=None, contact_email=None, contact_telephone=None):
        self.get_by_id(id_fournisseur)
        if nom:
            existing = self.dao.get_by_nom(nom)
            if existing and existing.id_fournisseur != id_fournisseur:
                raise ValueError(f"Le fournisseur '{nom}' existe déjà")
        return self.dao.update(id_fournisseur, nom, contact_nom, contact_email, contact_telephone)

    def delete(self, id_fournisseur):
        self.get_by_id(id_fournisseur)
        return self.dao.delete(id_fournisseur)