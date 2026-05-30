from app.database.initdb import get_db
from app.model.Colis import Colis

class ColisDAO:

    def _base_select(self):
        return """
            SELECT c.*,
                sc.libelle AS statut_libelle,
                u.fullName AS destinataire_nom,
                r.fullName AS receptionnaire_nom,
                bc.numero_commande AS numero_commande,
                d.nom AS departement_nom
            FROM colis c
            LEFT JOIN statut_colis sc ON c.statut_id = sc.id_statut
            LEFT JOIN utilisateur u ON c.destinataire_id = u.id_utilisateur
            LEFT JOIN utilisateur r ON c.receptionne_par = r.id_utilisateur
            LEFT JOIN bon_commande bc ON c.bon_commande_id = bc.id_bon_commande
            LEFT JOIN departement d ON bc.departement_id = d.id_departement
        """

    def _fetch_one(self, where, params=()):
        conn = get_db()
        row = conn.execute(self._base_select() + where, params).fetchone()
        return Colis(dict(row)) if row else None

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        rows = conn.execute(self._base_select() + where, params).fetchall()
        return [Colis(dict(r)) for r in rows]

    def get_all(self):
        return self._fetch_all()

    def get_by_id(self, id_colis):
        return self._fetch_one(" WHERE c.id_colis = ?", (id_colis,))

    def get_by_numero_suivi(self, numero_suivi):
        return self._fetch_one(" WHERE c.numero_suivi = ?", (numero_suivi,))

    def get_by_code_barres(self, code_barres):
        return self._fetch_one(" WHERE c.code_barres = ?", (code_barres,))

    def get_by_destinataire(self, destinataire_id):
        return self._fetch_all(" WHERE c.destinataire_id = ?", (destinataire_id,))

    def get_by_bon_commande(self, bon_commande_id):
        return self._fetch_all(" WHERE c.bon_commande_id = ?", (bon_commande_id,))

    def get_by_statut(self, statut_id):
        return self._fetch_all(" WHERE c.statut_id = ?", (statut_id,))

    def get_by_departement(self, departement_id):
        return self._fetch_all(" WHERE bc.departement_id = ?", (departement_id,))

    def create(self, bon_commande_id, statut_id, numero_suivi=None, code_barres=None,
               destinataire_id=None, commentaire=None, receptionne_par=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO colis (bon_commande_id, statut_id, numero_suivi, code_barres,
                               destinataire_id, commentaire, receptionne_par)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (bon_commande_id, statut_id, numero_suivi, code_barres,
              destinataire_id, commentaire, receptionne_par))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update_statut(self, id_colis, statut_id):
        conn = get_db()
        conn.execute("UPDATE colis SET statut_id = ? WHERE id_colis = ?", (statut_id, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    def update_reception(self, id_colis, receptionne_par, date_reception):
        conn = get_db()
        conn.execute("""
            UPDATE colis SET receptionne_par = ?, date_reception = ?
            WHERE id_colis = ?
        """, (receptionne_par, date_reception, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    def update_retrait(self, id_colis, date_retrait):
        conn = get_db()
        conn.execute("UPDATE colis SET date_retrait = ? WHERE id_colis = ?", (date_retrait, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    def update(self, id_colis, **kwargs):
        colis = self.get_by_id(id_colis)
        if not colis:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE colis
            SET statut_id = ?, numero_suivi = ?, code_barres = ?,
                destinataire_id = ?, commentaire = ?, receptionne_par = ?
            WHERE id_colis = ?
        """, (
            kwargs.get('statut_id', colis.statut_id),
            kwargs.get('numero_suivi', colis.numero_suivi),
            kwargs.get('code_barres', colis.code_barres),
            kwargs.get('destinataire_id', colis.destinataire_id),
            kwargs.get('commentaire', colis.commentaire),
            kwargs.get('receptionne_par', colis.receptionne_par),
            id_colis
        ))
        conn.commit()
        return self.get_by_id(id_colis)

    def delete(self, id_colis):
        conn = get_db()
        cursor = conn.execute("DELETE FROM colis WHERE id_colis = ?", (id_colis,))
        conn.commit()
        return cursor.rowcount