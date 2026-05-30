class Utilisateur:
    def __init__(self, dico):
        self.id_utilisateur = dico.get('id_utilisateur')
        self.uid_cas = dico.get('uid_cas')
        self.access_token_api_cas = dico.get('access_token_api_cas')
        self.full_name = dico.get('fullName')
        self.email = dico.get('email')
        self.password = dico.get('password')
        self.role_id = dico.get('role_id')
        self.departement_id = dico.get('departement_id')
        # Jointures optionnelles
        self.role_libelle = dico.get('role_libelle')
        self.departement_nom = dico.get('departement_nom')

    @property
    def is_cas(self):
        return self.uid_cas is not None

    @property
    def is_local(self):
        return self.password is not None

    def has_role(self, *roles):
        return self.role_libelle in roles

    def to_dict(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'uid_cas': self.uid_cas,
            'full_name': self.full_name,
            'email': self.email,
            'role_id': self.role_id,
            'role_libelle': self.role_libelle,
            'departement_id': self.departement_id,
            'departement_nom': self.departement_nom,
            'is_cas': self.is_cas,
            'is_local': self.is_local
        }