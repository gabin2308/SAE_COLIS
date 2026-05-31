class EvenementColis:
    def __init__(self, dico):
        self.id                   = dico.get('id')
        self.colis_id             = dico.get('colis_id')
        self.statut_id            = dico.get('statut_id')
        self.action               = dico.get('action')
        self.date_evenement       = dico.get('date_evenement')
        self.commentaire          = dico.get('commentaire')
        self.utilisateur_id       = dico.get('utilisateur_id')
        self.localisation         = dico.get('localisation')
        self.transporteur         = dico.get('transporteur')
        self.numero_livraison     = dico.get('numero_livraison')
        self.date_expedition      = dico.get('date_expedition')
        self.date_estimee_arrivee = dico.get('date_estimee_arrivee')
        # Jointures
        self.statut_libelle       = dico.get('statut_libelle')
        self.utilisateur_nom      = dico.get('utilisateur_nom')
        self.colis_numero_suivi   = dico.get('colis_numero_suivi')
 
    def to_dict(self):
        return {
            'id':                    self.id,
            'colis_id':              self.colis_id,
            'colis_numero_suivi':    self.colis_numero_suivi,
            'statut_id':             self.statut_id,
            'statut_libelle':        self.statut_libelle,
            'action':                self.action,
            'date_evenement':        self.date_evenement,
            'commentaire':           self.commentaire,
            'utilisateur_id':        self.utilisateur_id,
            'utilisateur_nom':       self.utilisateur_nom,
            'localisation':          self.localisation,
            'transporteur':          self.transporteur,
            'numero_livraison':      self.numero_livraison,
            'date_expedition':       self.date_expedition,
            'date_estimee_arrivee':  self.date_estimee_arrivee,
        }
