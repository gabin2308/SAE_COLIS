from app.dao.RoleDAO import RoleDAO

class RoleService:

    def __init__(self):
        self.dao = RoleDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_role):
        role = self.dao.get_by_id(id_role)
        if not role:
            raise ValueError(f"Rôle {id_role} introuvable")
        return role

    def get_by_libelle(self, libelle):
        role = self.dao.get_by_libelle(libelle)
        if not role:
            raise ValueError(f"Rôle '{libelle}' introuvable")
        return role

    def create(self, libelle):
        if not libelle or not libelle.strip():
            raise ValueError("Le libellé est requis")
        if self.dao.get_by_libelle(libelle):
            raise ValueError(f"Le rôle '{libelle}' existe déjà")
        return self.dao.create(libelle.strip())

    def update(self, id_role, libelle):
        if not libelle or not libelle.strip():
            raise ValueError("Le libellé est requis")
        self.get_by_id(id_role)  # vérifie existence
        existing = self.dao.get_by_libelle(libelle)
        if existing and existing.id_role != id_role:
            raise ValueError(f"Le rôle '{libelle}' existe déjà")
        return self.dao.update(id_role, libelle.strip())

    def delete(self, id_role):
        self.get_by_id(id_role)  # vérifie existence
        return self.dao.delete(id_role)