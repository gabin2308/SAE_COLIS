from app.dao.UtilisateurDAO import UtilisateurDAO as UserDAO


class UtilisateurService:

    def __init__(self):
        self.dao = UserDAO()

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create_user(self, full_name, email, password, role_id, departement_id):
        try:
            return self.dao.create_local(
                full_name,
                email,
                password,
                role_id,
                departement_id
            )
        except Exception as e:
            raise Exception(f"Erreur création utilisateur: {str(e)}")

    # ─────────────────────────────────────────
    # LOGIN (LOCAL)
    # ─────────────────────────────────────────

    def login(self, email, password):
            user = self.dao.get_by_email(email)

            if not user:
                return {"success": False, "message": "Utilisateur non trouvé"}

            if not self.dao.check_password(user, password):
                return {"success": False, "message": "Identifiants incorrects"}

            # Vérification du flag de changement de mot de passe
            if user.password_must_change:
                return {
                    "success": True, 
                    "must_change_password": True, 
                    "user": user.to_dict()
                }

            return {"success": True, "must_change_password": False, "user": user.to_dict()}
    # ─────────────────────────────────────────
    # CAS
    # ─────────────────────────────────────────

    def create_or_login_cas(
        self,
        uid_cas,
        access_token,
        full_name,
        email,
        role_id,
        departement_id=None
    ):
        try:
            return self.dao.create_or_link_cas(
                uid_cas,
                access_token,
                full_name,
                email,
                role_id,
                departement_id
            )
        except Exception as e:
            raise Exception(f"Erreur CAS: {str(e)}")

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_all_users(self):
        return self.dao.get_all()

    def get_user_by_id(self, id_utilisateur):
        return self.dao.get_by_id(id_utilisateur)

    def search_users(self, query):
        return self.dao.search(query)

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def update_user(
        self,
        id_utilisateur,
        full_name=None,
        email=None,
        role_id=None,
        departement_id=None
    ):
        try:
            return self.dao.update(
                id_utilisateur=id_utilisateur,
                full_name=full_name,
                email=email,
                role_id=role_id,
                departement_id=departement_id
            )
        except Exception as e:
            raise Exception(f"Erreur update utilisateur: {str(e)}")

    def update_password(self, id_utilisateur, new_password):
        try:
            return self.dao.update_password(id_utilisateur, new_password)
        except Exception as e:
            raise Exception(f"Erreur update password: {str(e)}")

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete_user(self, id_utilisateur):
        try:
            return self.dao.delete(id_utilisateur)
        except Exception as e:
            raise Exception(f"Erreur suppression utilisateur: {str(e)}")

    # ─────────────────────────────────────────
    # AUTH (API PROPRE)
    # ─────────────────────────────────────────

    def authenticate(self, email, password):
        result = self.login(email, password)

        if not result["success"]:
            return result

        # Retourne le résultat complet incluant must_change_password
        return {
            "success": True,
            "must_change_password": result.get("must_change_password", False),
            "user": result["user"]
        }
    
    def create_admin_managed_user(self, full_name, email, role_id, departement_id):
        try:
            # Appel de la méthode DAO créée précédemment
            return self.dao.create_initial_user(full_name, email, role_id, departement_id)
        except Exception as e:
            raise Exception(f"Erreur création admin: {str(e)}")