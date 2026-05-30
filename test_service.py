from app import app
from app.service.UserService import UserService


class TestUserService:

    def __init__(self):
        self.service = UserService()

    # =========================
    # CREATE USER
    # =========================
    def test_create_user(self):
        print("\n===== CREATE USER (SERVICE) =====")

        try:
            user = self.service.create_user(
                full_name="Utilisateur Test",
                email="test@example.com",
                password="password123",
                role_id=1,
                departement_id=1
            )

            print("Utilisateur créé :", user.to_dict())

        except Exception as e:
            print("Erreur création :", e)

    # =========================
    # LOGIN
    # =========================
    def test_login(self):
        print("\n===== LOGIN (SERVICE) =====")

        user = self.service.login("test@example.com", "password123")

        if user:
            print("Connexion OK :", user.to_dict())
        else:
            print("Connexion échouée")

    # =========================
    # GET ALL
    # =========================
    def test_get_all(self):
        print("\n===== USERS LIST (SERVICE) =====")

        users = self.service.get_all_users()

        for u in users:
            print(u.to_dict())

    # =========================
    # DELETE
    # =========================
    def test_delete(self, user_id):
        print("\n===== DELETE (SERVICE) =====")

        result = self.service.delete_user(user_id)

        if result:
            print("Utilisateur supprimé")
        else:
            print("Utilisateur introuvable")


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    with app.app_context():

        test = TestUserService()

        test.test_create_user()
        test.test_get_all()
        test.test_login()

        # test.test_delete(1)