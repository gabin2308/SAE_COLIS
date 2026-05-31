from app.dao.DevisDAO import DevisDAO

STATUTS_VALIDES = ('en_attente', 'accepte', 'refuse')

class DevisService:
    def __init__(self):
        self.dao = DevisDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_devis):
        devis = self.dao.get_by_id(id_devis)
        if not devis:
            raise ValueError(f"Devis {id_devis} introuvable")
        return devis

    def get_by_fournisseur(self, fournisseur_id):
        return self.dao.get_by_fournisseur(fournisseur_id)

    def get_by_createur(self, createur_id):
        return self.dao.get_by_createur(createur_id)

    def get_by_demande(self, demande_id):
        return self.dao.get_by_demande(demande_id)

    def get_by_statut(self, statut):
        if statut not in STATUTS_VALIDES:
            raise ValueError(f"Statut invalide, valeurs possibles : {STATUTS_VALIDES}")
        return self.dao.get_by_statut(statut)

    def create(self, fournisseur_id, createur_id, objet=None,
               montant_estime=None, fichier_pdf=None, demande_id=None):
        if not fournisseur_id or not createur_id:
            raise ValueError("fournisseur_id et createur_id sont requis")
        return self.dao.create(          # ✅ signature alignée, date gérée par le DAO
            fournisseur_id=fournisseur_id,
            createur_id=createur_id,
            objet=objet,
            montant_estime=montant_estime,
            fichier_pdf=fichier_pdf,
            demande_id=demande_id
        )

    def accepter(self, id_devis):
        self.get_by_id(id_devis)
        return self.dao.accepter(id_devis)   # ✅

    def refuser(self, id_devis):
        self.get_by_id(id_devis)
        return self.dao.refuser(id_devis)    # ✅

    def update(self, id_devis, objet=None, montant_estime=None, fichier_pdf=None):
        self.get_by_id(id_devis)
        return self.dao.update(id_devis, objet, montant_estime, fichier_pdf)  # ✅

    def delete(self, id_devis):
        self.get_by_id(id_devis)
        return self.dao.delete(id_devis)