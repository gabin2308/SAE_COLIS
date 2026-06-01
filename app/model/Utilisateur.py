class Utilisateur:
    def __init__(self, dico):
        self.id_utilisateur       = dico.get('id_utilisateur')
        self.uid_cas              = dico.get('uid_cas')
        self.access_token_api_cas = dico.get('access_token_api_cas')
        self.fullName             = dico.get('fullName')
        self.email                = dico.get('email')
        self.password             = dico.get('password')
        self.role_id              = dico.get('role_id')
        self.departement_id       = dico.get('departement_id')
        # Jointures
        self.role_nom             = dico.get('role_nom')
        self.departement_nom      = dico.get('departement_nom')
        self.password_must_change = dico.get('password_must_change', False)
    def to_dict(self):
        return {
            'id_utilisateur':  self.id_utilisateur,
            'uid_cas':         self.uid_cas,
            'access_token_api_cas': self.access_token_api_cas,
            'fullName':        self.fullName,
            'email':           self.email,
            'password':        self.password,
            'role_id':         self.role_id,
            'role_nom':        self.role_nom,
            'departement_id':  self.departement_id,
            'departement_nom': self.departement_nom,
            'password_must_change': self.password_must_change,
        }
