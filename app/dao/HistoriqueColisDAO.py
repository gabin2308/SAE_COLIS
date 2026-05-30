from app.database.initdb import get_db
from app.model.HistoriqueColis import HistoriqueColis

class HistoriqueColisDAO:

    def _base_select(self):
        return """
            SELECT h.*, u.fullName AS utilisateur_nom
            FROM historique_colis h
            LEFT JOIN utilisateur u ON h.utilisateur_id = u.id_utilisateur
        """

    def get_by_colis(self, id_colis):
        conn = get_db()
        rows = conn.execute(
            self._base_select() + " WHERE h.id_colis = ? ORDER BY h.date_action DESC",
            (id_colis,)
        ).fetchall()
        return [HistoriqueColis(dict(r)) for r in rows]

    def get_by_utilisateur(self, utilisateur_id):
        conn = get_db()
        rows = conn.execute(
            self._base_select() + " WHERE h.utilisateur_id = ? ORDER BY h.date_action DESC",
            (utilisateur_id,)
        ).fetchall()
        return [HistoriqueColis(dict(r)) for r in rows]

    def create(self, id_colis, action, utilisateur_id=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO historique_colis (id_colis, action, utilisateur_id)
            VALUES (?, ?, ?)
        """, (id_colis, action, utilisateur_id))
        conn.commit()
        return cursor.lastrowid