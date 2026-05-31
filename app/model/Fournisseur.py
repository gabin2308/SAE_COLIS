class Fournisseur:
    def __init__(self, dico):
        self.id_fournisseur         = dico.get('id_fournisseur')
        self.nom                    = dico.get('nom')
        self.siret                  = dico.get('siret')
        self.site_web               = dico.get('site_web')
        self.contact_nom            = dico.get('contact_nom')
        self.contact_email          = dico.get('contact_email')
        self.contact_telephone      = dico.get('contact_telephone')
        self.actif                  = dico.get('actif', 1)
        self.date_creation          = dico.get('date_creation')
        self.date_modification      = dico.get('date_modification')
        self.delai_livraison_jours  = dico.get('delai_livraison_jours')
        self.conditions_paiement    = dico.get('conditions_paiement')
        self.adresse_id             = dico.get('adresse_id')
        # Jointure
        self.adresse_ville          = dico.get('adresse_ville')
 
    def to_dict(self):
        return {
            'id_fournisseur':        self.id_fournisseur,
            'nom':                   self.nom,
            'siret':                 self.siret,
            'site_web':              self.site_web,
            'contact_nom':           self.contact_nom,
            'contact_email':         self.contact_email,
            'contact_telephone':     self.contact_telephone,
            'actif':                 self.actif,
            'date_creation':         self.date_creation,
            'date_modification':     self.date_modification,
            'delai_livraison_jours': self.delai_livraison_jours,
            'conditions_paiement':   self.conditions_paiement,
            'adresse_id':            self.adresse_id,
            'adresse_ville':         self.adresse_ville,
        }
