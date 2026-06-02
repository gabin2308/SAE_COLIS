from app.dao.UtilisateurDAO import UtilisateurDAO as UserDAO


class UtilisateurService:

    def __init__(self):
        self.dao = UserDAO()

    # ─────────────────────────────────────────
    # LOGIN (LOCAL)
    # ─────────────────────────────────────────

    def login(self, email, password):
        user = self.dao.get_by_email(email)

        if not user:
            return {"success": False, "message": "Utilisateur non trouvé"}

        if not self.dao.check_password(user, password):
            return {"success": False, "message": "Identifiants incorrects"}

        if user.password_must_change:
            return {"success": True, "must_change_password": True, "user": user.to_dict()}

        return {"success": True, "must_change_password": False, "user": user.to_dict()}

    # ─────────────────────────────────────────
    # CAS
    # ─────────────────────────────────────────

    def create_or_login_cas(self, uid_cas, access_token, full_name, email, role_id, departement_id=None):
        try:
            return self.dao.create_or_link_cas(uid_cas, access_token, full_name, email, role_id, departement_id)
        except Exception as e:
            raise Exception(f"Erreur CAS: {str(e)}")

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_utilisateur):
        return self.dao.get_by_id(id_utilisateur)

    def search(self, query):
        return self.dao.search(query)

    # ─────────────────────────────────────────
    # CREATE (admin — première connexion forcée)
    # Génère un mot de passe temporaire, password_must_change = 1
    # ─────────────────────────────────────────

    def create_initial_user(self, full_name, email, role_id, departement_id):
        if self.dao.get_by_email(email):
            raise ValueError("Email déjà utilisé")
        try:

            return self.dao.create_initial_user(full_name, email, role_id, departement_id)
        except ValueError:
            raise   # Email déjà utilisé → remonté tel quel au controller (409)
        except Exception as e:
            raise Exception(f"Erreur création utilisateur: {str(e)}")

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def update(self, id_utilisateur, full_name=None, email=None, role_id=None, departement_id=None):
        try:
            return self.dao.update(
                id_utilisateur=id_utilisateur,
                full_name=full_name,
                email=email,
                role_id=role_id,
                departement_id=departement_id,
            )
        except ValueError:
            raise   # Email déjà utilisé → 409
        except Exception as e:
            raise Exception(f"Erreur mise à jour utilisateur: {str(e)}")

    def update_password(self, id_utilisateur, new_password):
        try:
            return self.dao.update_password(id_utilisateur, new_password)
        except Exception as e:
            raise Exception(f"Erreur mise à jour mot de passe: {str(e)}")

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_utilisateur):
        try:
            return self.dao.delete(id_utilisateur)
        except Exception as e:
            raise Exception(f"Erreur suppression utilisateur: {str(e)}")
        

    def create_user(self, full_name, email, password, role_id, departement_id):
        try:
            # Appel au DAO pour créer l'utilisateur avec le mot de passe fourni
            return self.dao.create_user(full_name, email, password, role_id, departement_id)
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Erreur création utilisateur: {str(e)}")