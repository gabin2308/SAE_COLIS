class Devis:
    def __init__(self, dico):
        self.id_devis = dico.get('id_devis')
        self.date_demande = dico.get('date_demande')
        self.objet = dico.get('objet')
        self.montant_estime = dico.get('montant_estime')
        self.fichier_pdf = dico.get('fichier_pdf')
        self.statut = dico.get('statut', 'en_attente')
        self.fournisseur_id = dico.get('fournisseur_id')
        self.createur_id = dico.get('createur_id')
        # Jointures optionnelles
        self.fournisseur_nom = dico.get('fournisseur_nom')
        self.createur_nom = dico.get('createur_nom')

    STATUTS = ['en_attente', 'accepte', 'refuse']

    def to_dict(self):
        return {
            'id_devis': self.id_devis,
            'date_demande': str(self.date_demande) if self.date_demande else None,
            'objet': self.objet,
            'montant_estime': float(self.montant_estime) if self.montant_estime else None,
            'statut': self.statut,
            'fournisseur_id': self.fournisseur_id,
            'fournisseur_nom': self.fournisseur_nom,
            'createur_id': self.createur_id,
            'createur_nom': self.createur_nom
        }