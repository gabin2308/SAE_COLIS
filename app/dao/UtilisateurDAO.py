from app.database.initdb import get_db
from app.model.Utilisateur import Utilisateur
from app import bcrypt
import secrets


class UtilisateurDAO:

    def _base_select(self):
        return """
            SELECT u.*, r.libelle AS role_nom, d.nom AS departement_nom
            FROM utilisateur u
            JOIN role r ON u.role_id = r.id_role
            LEFT JOIN departement d ON u.departement_id = d.id_departement
        """

    def _fetch_one(self, where, params):
        conn = get_db()
        return conn.execute(self._base_select() + where, params).fetchone()

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        return conn.execute(self._base_select() + where, params).fetchall()

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_all(self):
        return [Utilisateur(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_utilisateur):
        row = self._fetch_one(" WHERE u.id_utilisateur = ?", (id_utilisateur,))
        return Utilisateur(dict(row)) if row else None

    def get_by_uid_cas(self, uid_cas):
        row = self._fetch_one(" WHERE u.uid_cas = ?", (uid_cas,))
        return Utilisateur(dict(row)) if row else None

    def get_by_email(self, email):
        row = self._fetch_one(" WHERE u.email = ?", (email,))
        return Utilisateur(dict(row)) if row else None

    def get_by_role(self, role_libelle):
        rows = self._fetch_all(" WHERE r.libelle = ?", (role_libelle,))
        return [Utilisateur(dict(r)) for r in rows]

    def get_by_departement(self, departement_id):
        rows = self._fetch_all(" WHERE u.departement_id = ?", (departement_id,))
        return [Utilisateur(dict(r)) for r in rows]

    def get_by_cas_or_email(self, email, uid_cas):
        row = self._fetch_one(
            " WHERE u.email = ? OR u.uid_cas = ?",
            (email, uid_cas)
        )
        return Utilisateur(dict(row)) if row else None

    def get_responsable_departement(self, departement_id):
        """Retourne le responsable d'un département.
        Utile pour notifier le responsable quand un lecteur soumet une demande."""
        row = self._fetch_one(
            " WHERE u.departement_id = ? AND r.libelle = 'responsable_departement' LIMIT 1",
            (departement_id,)
        )
        return Utilisateur(dict(row)) if row else None

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(
            " WHERE u.fullName LIKE ? OR u.email LIKE ? OR u.uid_cas LIKE ?",
            (q, q, q)
        )
        return [Utilisateur(dict(r)) for r in rows]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create_local(self, full_name, email, password, role_id, departement_id=None):
        if not departement_id:
            raise ValueError("departement_id obligatoire")

        conn = get_db()

        if self.get_by_email(email):
            raise ValueError("Email déjà utilisé")

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = conn.execute("""
            INSERT INTO utilisateur (fullName, email, password, role_id, departement_id)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, email, password_hash, role_id, departement_id))

        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def create_cas(self, *args, **kwargs):
        return self.create_or_link_cas(*args, **kwargs)

    def create_or_link_cas(self, uid_cas, access_token, full_name, email, role_id, departement_id=None):
        conn = get_db()

        existing_cas = self.get_by_uid_cas(uid_cas)
        if existing_cas and existing_cas.email != email:
            raise ValueError("CAS déjà lié à un autre compte")

        user = self.get_by_email(email)

        if user:
            if user.uid_cas and user.uid_cas != uid_cas:
                raise ValueError("Compte déjà lié à un autre CAS")

            conn.execute("""
                UPDATE utilisateur
                SET uid_cas = ?, access_token_api_cas = ?
                WHERE id_utilisateur = ?
            """, (uid_cas, access_token, user.id_utilisateur))

            conn.commit()
            return self.get_by_id(user.id_utilisateur)

        cursor = conn.execute("""
            INSERT INTO utilisateur (uid_cas, access_token_api_cas, fullName, email, role_id, departement_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (uid_cas, access_token, full_name, email, role_id, departement_id))

        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def update(self, id_utilisateur, full_name=None, email=None, role_id=None, departement_id=None):
        user = self.get_by_id(id_utilisateur)
        if not user:
            return None

        if email and email != user.email:
            if self.get_by_email(email):
                raise ValueError("Email déjà utilisé")

        conn = get_db()
        conn.execute("""
            UPDATE utilisateur
            SET fullName = ?, email = ?, role_id = ?, departement_id = ?
            WHERE id_utilisateur = ?
        """, (
            full_name      or user.fullName,
            email          or user.email,
            role_id        or user.role_id,
            departement_id or user.departement_id,
            id_utilisateur
        ))

        conn.commit()
        return self.get_by_id(id_utilisateur)

    def update_password(self, id_utilisateur, nouveau_password):
        conn = get_db()
        conn.execute("""
            UPDATE utilisateur SET password = ?
            WHERE id_utilisateur = ?
        """, (bcrypt.generate_password_hash(nouveau_password).decode('utf-8'), id_utilisateur))

        conn.commit()
        return self.get_by_id(id_utilisateur)

    def update_token(self, uid_cas, nouveau_token):
        conn = get_db()
        cursor = conn.execute("""
            UPDATE utilisateur
            SET access_token_api_cas = ?
            WHERE uid_cas = ?
        """, (nouveau_token, uid_cas))

        conn.commit()
        return cursor.rowcount

    def link_cas(self, id_utilisateur, uid_cas, access_token):
        conn = get_db()
        conn.execute("""
            UPDATE utilisateur
            SET uid_cas = ?, access_token_api_cas = ?
            WHERE id_utilisateur = ?
        """, (uid_cas, access_token, id_utilisateur))

        conn.commit()
        return self.get_by_id(id_utilisateur)

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_utilisateur):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM utilisateur WHERE id_utilisateur = ?",
            (id_utilisateur,)
        )
        conn.commit()
        return cursor.rowcount

    # ─────────────────────────────────────────
    # UTILITAIRES
    # ─────────────────────────────────────────

    def check_password(self, utilisateur, password):
        if not utilisateur or not utilisateur.password:
            return False
        return bcrypt.check_password_hash(utilisateur.password, password)

    def is_cas_linked(self, user):
        return bool(user and user.uid_cas)
    

    def update_password(self, id_utilisateur, nouveau_password):
        conn = get_db()
        # 1. Mise à jour du mot de passe haché
        conn.execute("""
            UPDATE utilisateur 
            SET password = ?, password_must_change = 0
            WHERE id_utilisateur = ?
        """, (bcrypt.generate_password_hash(nouveau_password).decode('utf-8'), id_utilisateur))

        conn.commit()
        return self.get_by_id(id_utilisateur)
    
    def create_initial_user(self, full_name, email, role_id, departement_id):
        # 1. Générer un mot de passe temporaire complexe (inconnu de l'utilisateur)
        temp_password = secrets.token_urlsafe(32)
        password_hash = bcrypt.generate_password_hash(temp_password).decode('utf-8')
        
        conn = get_db()
        
        # 2. Insertion avec password_must_change = 1
        cursor = conn.execute("""
            INSERT INTO utilisateur (fullName, email, password, role_id, departement_id, password_must_change)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (full_name, email, password_hash, role_id, departement_id))
        
        conn.commit()
        return self.get_by_id(cursor.lastrowid)