from app.database.initdb import get_db
from app.model.Fournisseur import Fournisseur

class FournisseurDAO:

    def get_all(self):
        conn = get_db()
        rows = conn.execute("SELECT * FROM fournisseur").fetchall()
        return [Fournisseur(dict(r)) for r in rows]

    def get_by_id(self, id_fournisseur):
        conn = get_db()
        row = conn.execute("SELECT * FROM fournisseur WHERE id_fournisseur = ?", (id_fournisseur,)).fetchone()
        return Fournisseur(dict(row)) if row else None

    def get_by_nom(self, nom):
        conn = get_db()
        row = conn.execute("SELECT * FROM fournisseur WHERE nom = ?", (nom,)).fetchone()
        return Fournisseur(dict(row)) if row else None

    def create(self, nom, contact_nom=None, contact_email=None, contact_telephone=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO fournisseur (nom, contact_nom, contact_email, contact_telephone)
            VALUES (?, ?, ?, ?)
        """, (nom, contact_nom, contact_email, contact_telephone))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update(self, id_fournisseur, nom=None, contact_nom=None, contact_email=None, contact_telephone=None):
        f = self.get_by_id(id_fournisseur)
        if not f:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE fournisseur
            SET nom = ?, contact_nom = ?, contact_email = ?, contact_telephone = ?
            WHERE id_fournisseur = ?
        """, (
            nom or f.nom,
            contact_nom or f.contact_nom,
            contact_email or f.contact_email,
            contact_telephone or f.contact_telephone,
            id_fournisseur
        ))
        conn.commit()
        return self.get_by_id(id_fournisseur)

    def delete(self, id_fournisseur):
        conn = get_db()
        cursor = conn.execute("DELETE FROM fournisseur WHERE id_fournisseur = ?", (id_fournisseur,))
        conn.commit()
        return cursor.rowcount