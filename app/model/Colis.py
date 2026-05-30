class Colis:
    def __init__(self, dico):
        self.id_colis = dico.get('id_colis')
        self.bon_commande_id = dico.get('bon_commande_id')
        self.statut_id = dico.get('statut_id')
        self.numero_suivi = dico.get('numero_suivi')
        self.code_barres = dico.get('code_barres')
        self.destinataire_id = dico.get('destinataire_id')
        self.date_reception = dico.get('date_reception')
        self.date_retrait = dico.get('date_retrait')
        self.commentaire = dico.get('commentaire')
        self.receptionne_par = dico.get('receptionne_par')
        # Jointures optionnelles
        self.statut_libelle = dico.get('statut_libelle')
        self.destinataire_nom = dico.get('destinataire_nom')
        self.receptionnaire_nom = dico.get('receptionnaire_nom')
        self.numero_commande = dico.get('numero_commande')
        self.departement_nom = dico.get('departement_nom')

    def to_dict(self):
        return {
            'id_colis': self.id_colis,
            'bon_commande_id': self.bon_commande_id,
            'numero_commande': self.numero_commande,
            'statut_id': self.statut_id,
            'statut_libelle': self.statut_libelle,
            'numero_suivi': self.numero_suivi,
            'code_barres': self.code_barres,
            'destinataire_id': self.destinataire_id,
            'destinataire_nom': self.destinataire_nom,
            'date_reception': str(self.date_reception) if self.date_reception else None,
            'date_retrait': str(self.date_retrait) if self.date_retrait else None,
            'commentaire': self.commentaire,
            'receptionne_par': self.receptionne_par,
            'receptionnaire_nom': self.receptionnaire_nom,
            'departement_nom': self.departement_nom
        }