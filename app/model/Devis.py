class Devis:
    def __init__(self, dico):
        self.id_devis        = dico.get('id_devis')
        self.date_demande    = dico.get('date_demande')
        self.objet           = dico.get('objet')
        self.montant_estime  = dico.get('montant_estime')
        self.fichier_pdf     = dico.get('fichier_pdf')
        self.statut          = dico.get('statut', 'en_attente')
        self.fournisseur_id  = dico.get('fournisseur_id')
        self.createur_id     = dico.get('createur_id')
        self.demande_id      = dico.get('demande_id')
        # Jointures
        self.fournisseur_nom = dico.get('fournisseur_nom')
        self.createur_nom    = dico.get('createur_nom')
        self.demande_objet   = dico.get('demande_objet')
 
    def to_dict(self):
        return {
            'id_devis':       self.id_devis,
            'date_demande':   self.date_demande,
            'objet':          self.objet,
            'montant_estime': self.montant_estime,
            'fichier_pdf':    self.fichier_pdf,
            'statut':         self.statut,
            'fournisseur_id': self.fournisseur_id,
            'fournisseur_nom':self.fournisseur_nom,
            'createur_id':    self.createur_id,
            'createur_nom':   self.createur_nom,
            'demande_id':     self.demande_id,
            'demande_objet':  self.demande_objet,
        }
