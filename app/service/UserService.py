from app.dao.UserDAO import UtilisateurDAO as UserDAO


class UserService:

    def __init__(self):
        self.dao = UserDAO()

   
    def create_user(self, full_name, email, password, role_id, departement_id):
        try:
            return self.dao.create_local(full_name, email, password, role_id, departement_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erreur création utilisateur: {str(e)}")

   
    def login(self, email, password):
        user = self.dao.get_by_email(email)

        if not user:
            return None

        if not self.dao.check_password(user, password):
            return None

        return user

    
    def create_or_login_cas(self, uid_cas, access_token, full_name, email, role_id, departement_id=None):
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

   
    def get_all_users(self):
        return self.dao.get_all()

    def get_user_by_id(self, id_utilisateur):
        return self.dao.get_by_id(id_utilisateur)

    def search_users(self, query):
        return self.dao.search(query)

    def update_user(self, id_utilisateur, full_name=None, email=None, role_id=None, departement_id=None):
        try:
            return self.dao.update(
                id_utilisateur,
                full_name,
                email,
                role_id,
                departement_id
            )
        except Exception as e:
            raise Exception(f"Erreur update utilisateur: {str(e)}")

    def update_password(self, id_utilisateur, new_password):
        return self.dao.update_password(id_utilisateur, new_password)

   
    def delete_user(self, id_utilisateur):
        try:
            return self.dao.delete(id_utilisateur)
        except Exception as e:
            raise Exception(f"Erreur suppression utilisateur: {str(e)}")

    
    def authenticate(self, email, password):
        """
        Version propre pour API login
        """
        user = self.connect_user(email, password)

        if not user:
            return {
                "success": False,
                "message": "Identifiants incorrects"
            }

        return {
            "success": True,
            "user": user
        }