
class BonCommande:
    def __init__(self, dico):
        self.id_bon_commande = dico.get('id_bon_commande')
        self.numero_commande = dico.get('numero_commande')
        self.date_commande = dico.get('date_commande')
        self.date_estimee_livraison = dico.get('date_estimee_livraison')
        self.montant_estime = dico.get('montant_estime', 0)
        self.statut = dico.get('statut', 'en_preparation')
        self.departement_id = dico.get('departement_id')
        self.fournisseur_id = dico.get('fournisseur_id')
        self.createur_id = dico.get('createur_id')
        self.devis_id = dico.get('devis_id')
        self.commentaire = dico.get('commentaire')
        # Jointures optionnelles
        self.departement_nom = dico.get('departement_nom')
        self.fournisseur_nom = dico.get('fournisseur_nom')
        self.createur_nom = dico.get('createur_nom')

    STATUTS = ['en_preparation', 'en_cours', 'livree', 'annulee']

    def to_dict(self):
        return {
            'id_bon_commande': self.id_bon_commande,
            'numero_commande': self.numero_commande,
            'date_commande': str(self.date_commande) if self.date_commande else None,
            'date_estimee_livraison': str(self.date_estimee_livraison) if self.date_estimee_livraison else None,
            'montant_estime': float(self.montant_estime) if self.montant_estime else 0,
            'statut': self.statut,
            'departement_id': self.departement_id,
            'departement_nom': self.departement_nom,
            'fournisseur_id': self.fournisseur_id,
            'fournisseur_nom': self.fournisseur_nom,
            'createur_id': self.createur_id,
            'createur_nom': self.createur_nom,
            'devis_id': self.devis_id,
            'commentaire': self.commentaire
        }