class Colis:
    def __init__(self, dico):
        self.id_colis         = dico.get('id_colis')
        self.bon_commande_id  = dico.get('bon_commande_id')
        self.statut_id        = dico.get('statut_id')
        self.numero_suivi     = dico.get('numero_suivi')
        self.code_barres      = dico.get('code_barres')
        self.qr_payload       = dico.get('qr_payload')
        self.qr_image_path    = dico.get('qr_image_path')
        self.destinataire_id  = dico.get('destinataire_id')
        self.date_reception   = dico.get('date_reception')
        self.date_retrait     = dico.get('date_retrait')
        self.commentaire      = dico.get('commentaire')
        self.receptionne_par  = dico.get('receptionne_par')
        # Jointures
        self.statut_libelle       = dico.get('statut_libelle')
        self.destinataire_nom     = dico.get('destinataire_nom')
        self.receptionne_par_nom  = dico.get('receptionne_par_nom')
        self.numero_commande      = dico.get('numero_commande')
 
    def to_dict(self):
        return {
            'id_colis':              self.id_colis,
            'bon_commande_id':       self.bon_commande_id,
            'numero_commande':       self.numero_commande,
            'statut_id':             self.statut_id,
            'statut_libelle':        self.statut_libelle,
            'numero_suivi':          self.numero_suivi,
            'code_barres':           self.code_barres,
            'qr_payload':            self.qr_payload,
            'qr_image_path':         self.qr_image_path,
            'destinataire_id':       self.destinataire_id,
            'destinataire_nom':      self.destinataire_nom,
            'date_reception':        self.date_reception,
            'date_retrait':          self.date_retrait,
            'commentaire':           self.commentaire,
            'receptionne_par':       self.receptionne_par,
            'receptionne_par_nom':   self.receptionne_par_nom,
        }
