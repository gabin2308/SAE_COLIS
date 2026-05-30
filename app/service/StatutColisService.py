from app.dao.StatutColisDAO import StatutColisDAO

class StatutColisService:

    def __init__(self):
        self.dao = StatutColisDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_statut):
        statut = self.dao.get_by_id(id_statut)
        if not statut:
            raise ValueError(f"Statut {id_statut} introuvable")
        return statut

    def create(self, libelle):
        if not libelle or not libelle.strip():
            raise ValueError("Le libellé est requis")
        if self.dao.get_by_libelle(libelle):
            raise ValueError(f"Le statut '{libelle}' existe déjà")
        return self.dao.create(libelle.strip())

    def delete(self, id_statut):
        self.get_by_id(id_statut)
        return self.dao.delete(id_statut)