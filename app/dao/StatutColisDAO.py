from app.database.initdb import get_db
from app.model.StatutColis import StatutColis

class StatutColisDAO:

    def get_all(self):
        conn = get_db()
        rows = conn.execute("SELECT * FROM statut_colis").fetchall()
        return [StatutColis(dict(r)) for r in rows]

    def get_by_id(self, id_statut):
        conn = get_db()
        row = conn.execute("SELECT * FROM statut_colis WHERE id_statut = ?",
                           (id_statut,)).fetchone()
        return StatutColis(dict(row)) if row else None

    def get_by_libelle(self, libelle):
        conn = get_db()
        row = conn.execute("SELECT * FROM statut_colis WHERE libelle = ?",
                           (libelle,)).fetchone()
        return StatutColis(dict(row)) if row else None

    def create(self, libelle):
        conn = get_db()
        cursor = conn.execute("INSERT INTO statut_colis (libelle) VALUES (?)", (libelle,))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def delete(self, id_statut):
        conn = get_db()
        cursor = conn.execute("DELETE FROM statut_colis WHERE id_statut = ?", (id_statut,))
        conn.commit()
        return cursor.rowcount