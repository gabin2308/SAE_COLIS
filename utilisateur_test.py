from app import app
from app.dao.UtilisateurDAO import UtilisateurDAO

with app.app_context():

    dao = UtilisateurDAO()

    print("\n========== TEST UtilisateurDAO ==========\n")

    # -------------------------------------------------
    # CREATE LOCAL
    # -------------------------------------------------
    print("1. CREATE LOCAL")

    try:
        user = dao.create_local(
            full_name="Utilisateur Test",
            email="test.dao@test.fr",
            password="password123",
            role_id=1,
            departement_id=1
        )

        print("Utilisateur créé")
        print(user.to_dict())

    except Exception as e:
        print("Erreur :", e)

    # -------------------------------------------------
    # GET BY EMAIL
    # -------------------------------------------------
    print("\n2. GET BY EMAIL")

    user = dao.get_by_email("test.dao@test.fr")

    if user:
        print(user.to_dict())

    # -------------------------------------------------
    # GET BY ID
    # -------------------------------------------------
    print("\n3. GET BY ID")

    if user:
        user_id = user.id_utilisateur

        found = dao.get_by_id(user_id)

        print(found.to_dict())

    # -------------------------------------------------
    # GET ALL
    # -------------------------------------------------
    print("\n4. GET ALL")

    users = dao.get_all()

    print(f"{len(users)} utilisateur(s) trouvé(s)")

    for u in users:
        print(u.to_dict())

    # -------------------------------------------------
    # CHECK PASSWORD
    # -------------------------------------------------
    print("\n5. CHECK PASSWORD")

    print(
        "Bon mot de passe :",
        dao.check_password(user, "password123")
    )

    print(
        "Mauvais mot de passe :",
        dao.check_password(user, "abcdef")
    )

    # -------------------------------------------------
    # UPDATE USER
    # -------------------------------------------------
    print("\n6. UPDATE")

    updated = dao.update(
        user.id_utilisateur,
        full_name="Utilisateur Modifié"
    )

    print(updated.to_dict())

    # -------------------------------------------------
    # UPDATE PASSWORD
    # -------------------------------------------------
    print("\n7. UPDATE PASSWORD")

    dao.update_password(
        user.id_utilisateur,
        "nouveauPassword"
    )

    user = dao.get_by_id(user.id_utilisateur)

    print(
        "Nouveau mot de passe OK :",
        dao.check_password(user, "nouveauPassword")
    )

    # -------------------------------------------------
    # CREATE CAS
    # -------------------------------------------------
    print("\n8. CREATE CAS")

    try:

        cas_user = dao.create_or_link_cas(
            uid_cas="cas_test_001",
            access_token="token123",
            full_name="Utilisateur CAS",
            email="cas@test.fr",
            role_id=1,
            departement_id=1
        )

        print(cas_user.to_dict())

    except Exception as e:
        print("Erreur :", e)

    # -------------------------------------------------
    # GET BY UID CAS
    # -------------------------------------------------
    print("\n9. GET BY UID CAS")

    cas_user = dao.get_by_uid_cas("cas_test_001")

    if cas_user:
        print(cas_user.to_dict())

    # -------------------------------------------------
    # UPDATE TOKEN
    # -------------------------------------------------
    print("\n10. UPDATE TOKEN")

    nb = dao.update_token(
        "cas_test_001",
        "nouveau_token_456"
    )

    print("Lignes modifiées :", nb)

    # -------------------------------------------------
    # LINK CAS
    # -------------------------------------------------
    print("\n11. LINK CAS")

    if user:

        linked = dao.link_cas(
            user.id_utilisateur,
            "cas_linked_999",
            "token_linked"
        )

        print(linked.to_dict())

    # -------------------------------------------------
    # GET BY ROLE
    # -------------------------------------------------
    print("\n12. GET BY ROLE")

    admins = dao.get_by_role("administrateur")

    for admin in admins:
        print(admin.to_dict())

    # -------------------------------------------------
    # GET BY DEPARTEMENT
    # -------------------------------------------------
    print("\n13. GET BY DEPARTEMENT")

    users_dep = dao.get_by_departement(1)

    for u in users_dep:
        print(u.to_dict())

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------
    print("\n14. SEARCH")

    results = dao.search("Utilisateur")

    for r in results:
        print(r.to_dict())

    # -------------------------------------------------
    # GET BY CAS OR EMAIL
    # -------------------------------------------------
    print("\n15. GET BY CAS OR EMAIL")

    result = dao.get_by_cas_or_email(
        "test.dao@test.fr",
        "cas_linked_999"
    )

    if result:
        print(result.to_dict())

    # -------------------------------------------------
    # IS CAS LINKED
    # -------------------------------------------------
    print("\n16. IS CAS LINKED")

    print(
        dao.is_cas_linked(result)
    )

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------
    print("\n17. DELETE")

    if user:

        deleted = dao.delete(
            user.id_utilisateur
        )

        print(
            "Lignes supprimées :",
            deleted
        )

    print("\n========== FIN TEST ==========\n")