from app.database.initdb import get_db
from app.model.Departement import Departement

class DepartementDAO:

    def get_all(self):
        conn = get_db()
        rows = conn.execute("SELECT * FROM departement").fetchall()
        return [Departement(dict(r)) for r in rows]

    def get_by_id(self, id_departement):
        conn = get_db()
        row = conn.execute("SELECT * FROM departement WHERE id_departement = ?", (id_departement,)).fetchone()
        return Departement(dict(row)) if row else None

    def get_by_nom(self, nom):
        conn = get_db()
        row = conn.execute("SELECT * FROM departement WHERE nom = ?", (nom,)).fetchone()
        return Departement(dict(row)) if row else None

    def create(self, nom, telephone=None, budget_total=0):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO departement (nom, telephone, budget_total, budget_utilise)
            VALUES (?, ?, ?, 0)
        """, (nom, telephone, budget_total))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update(self, id_departement, nom=None, telephone=None, budget_total=None):
        dep = self.get_by_id(id_departement)
        if not dep:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE departement
            SET nom = ?, telephone = ?, budget_total = ?
            WHERE id_departement = ?
        """, (
            nom or dep.nom,
            telephone or dep.telephone,
            budget_total if budget_total is not None else dep.budget_total,
            id_departement
        ))
        conn.commit()
        return self.get_by_id(id_departement)

    def update_budget_utilise(self, id_departement, montant):
        conn = get_db()
        conn.execute("""
            UPDATE departement
            SET budget_utilise = budget_utilise + ?
            WHERE id_departement = ?
        """, (montant, id_departement))
        conn.commit()
        return self.get_by_id(id_departement)

    def delete(self, id_departement):
        conn = get_db()
        cursor = conn.execute("DELETE FROM departement WHERE id_departement = ?", (id_departement,))
        conn.commit()
        return cursor.rowcount