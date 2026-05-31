from app.dao.FournisseurDAO import FournisseurDAO

class FournisseurService:
    def __init__(self):
        self.dao = FournisseurDAO()

    def get_all(self, actif_seulement=True):
        return self.dao.get_all(actif_seulement)

    def get_by_id(self, id_fournisseur):
        f = self.dao.get_by_id(id_fournisseur)
        if not f:
            raise ValueError(f"Fournisseur {id_fournisseur} introuvable")
        return f

    def search(self, query):
        return self.dao.search(query)

    def create(self, nom, siret=None, site_web=None, contact_nom=None,
               contact_email=None, contact_telephone=None,
               delai_livraison_jours=None, conditions_paiement=None):
        if not nom or not nom.strip():
            raise ValueError("Le nom est requis")
        if siret and self.dao.get_by_siret(siret):  # ✅ unicité sur siret
            raise ValueError(f"Un fournisseur avec le SIRET '{siret}' existe déjà")
        return self.dao.create(
            nom=nom.strip(),
            siret=siret,
            site_web=site_web,
            contact_nom=contact_nom,
            contact_email=contact_email,
            contact_telephone=contact_telephone,
            delai_livraison_jours=delai_livraison_jours,
            conditions_paiement=conditions_paiement
        )

    def update(self, id_fournisseur, nom=None, site_web=None, contact_nom=None,
               contact_email=None, contact_telephone=None,
               delai_livraison_jours=None, conditions_paiement=None):
        self.get_by_id(id_fournisseur)
        return self.dao.update(
            id_fournisseur,
            nom=nom,
            site_web=site_web,
            contact_nom=contact_nom,
            contact_email=contact_email,
            contact_telephone=contact_telephone,
            delai_livraison_jours=delai_livraison_jours,
            conditions_paiement=conditions_paiement
        )

    def desactiver(self, id_fournisseur):       # ✅ exposé
        self.get_by_id(id_fournisseur)
        return self.dao.desactiver(id_fournisseur)

    def reactiver(self, id_fournisseur):        # ✅ exposé
        self.get_by_id(id_fournisseur)
        return self.dao.reactiver(id_fournisseur)

    def delete(self, id_fournisseur):
        self.get_by_id(id_fournisseur)
        return self.dao.delete(id_fournisseur)