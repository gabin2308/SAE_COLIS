from app.database.initdb import get_db
from app.model.Role import Role

class RoleDAO:

    def get_all(self):
        conn = get_db()
        rows = conn.execute("SELECT * FROM role").fetchall()
        return [Role(dict(r)) for r in rows]

    def get_by_id(self, id_role):
        conn = get_db()
        row = conn.execute("SELECT * FROM role WHERE id_role = ?", (id_role,)).fetchone()
        return Role(dict(row)) if row else None

    def get_by_libelle(self, libelle):
        conn = get_db()
        row = conn.execute("SELECT * FROM role WHERE libelle = ?", (libelle,)).fetchone()
        return Role(dict(row)) if row else None

    def create(self, libelle):
        conn = get_db()
        cursor = conn.execute("INSERT INTO role (libelle) VALUES (?)", (libelle,))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update(self, id_role, libelle):
        conn = get_db()
        conn.execute("UPDATE role SET libelle = ? WHERE id_role = ?", (libelle, id_role))
        conn.commit()
        return self.get_by_id(id_role)

    def delete(self, id_role):
        conn = get_db()
        cursor = conn.execute("DELETE FROM role WHERE id_role = ?", (id_role,))
        conn.commit()
        return cursor.rowcount