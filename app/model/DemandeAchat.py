class DemandeAchat:
    def __init__(self, dico):
        self.id_demande = dico.get('id_demande')
        self.objet = dico.get('objet')
        self.description = dico.get('description')
        self.montant_estime = dico.get('montant_estime')
        self.statut = dico.get('statut', 'en_attente')
        self.date_demande = dico.get('date_demande')
        self.date_traitement = dico.get('date_traitement')
        self.commentaire_responsable = dico.get('commentaire_responsable')
        self.demandeur_id = dico.get('demandeur_id')
        self.departement_id = dico.get('departement_id')
        # Jointures
        self.demandeur_nom = dico.get('demandeur_nom')
        self.departement_nom = dico.get('departement_nom')

    STATUTS = ['en_attente', 'approuvee', 'refusee']

    def to_dict(self):
        return {
            'id_demande': self.id_demande,
            'objet': self.objet,
            'description': self.description,
            'montant_estime': float(self.montant_estime) if self.montant_estime else None,
            'statut': self.statut,
            'date_demande': str(self.date_demande) if self.date_demande else None,
            'date_traitement': str(self.date_traitement) if self.date_traitement else None,
            'commentaire_responsable': self.commentaire_responsable,
            'demandeur_id': self.demandeur_id,
            'demandeur_nom': self.demandeur_nom,
            'departement_id': self.departement_id,
            'departement_nom': self.departement_nom
        }