from app.database.initdb import get_db
from app.model.DemandeAchat import DemandeAchat

class DemandeAchatDAO:

    def _base_select(self):
        return """
            SELECT da.*,
                u.fullName AS demandeur_nom,
                d.nom AS departement_nom
            FROM demande_achat da
            LEFT JOIN utilisateur u ON da.demandeur_id = u.id_utilisateur
            LEFT JOIN departement d ON da.departement_id = d.id_departement
        """

    def _fetch_one(self, where, params=()):
        conn = get_db()
        row = conn.execute(self._base_select() + where, params).fetchone()
        return DemandeAchat(dict(row)) if row else None

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        rows = conn.execute(self._base_select() + where, params).fetchall()
        return [DemandeAchat(dict(r)) for r in rows]

    def get_all(self):
        return self._fetch_all(" ORDER BY da.date_demande DESC")

    def get_by_id(self, id_demande):
        return self._fetch_one(" WHERE da.id_demande = ?", (id_demande,))

    def get_by_demandeur(self, demandeur_id):
        return self._fetch_all(" WHERE da.demandeur_id = ? ORDER BY da.date_demande DESC",
                               (demandeur_id,))

    def get_by_departement(self, departement_id):
        return self._fetch_all(" WHERE da.departement_id = ? ORDER BY da.date_demande DESC",
                               (departement_id,))

    def get_by_statut(self, statut):
        return self._fetch_all(" WHERE da.statut = ? ORDER BY da.date_demande DESC",
                               (statut,))

    def get_en_attente_departement(self, departement_id):
        return self._fetch_all("""
            WHERE da.departement_id = ? AND da.statut = 'en_attente'
            ORDER BY da.date_demande ASC
        """, (departement_id,))

    def create(self, objet, demandeur_id, departement_id,
               description=None, montant_estime=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO demande_achat (objet, description, montant_estime,
                                       demandeur_id, departement_id)
            VALUES (?, ?, ?, ?, ?)
        """, (objet, description, montant_estime, demandeur_id, departement_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update_statut(self, id_demande, statut, commentaire_responsable=None):
        from datetime import datetime
        conn = get_db()
        conn.execute("""
            UPDATE demande_achat
            SET statut = ?, date_traitement = ?, commentaire_responsable = ?
            WHERE id_demande = ?
        """, (statut, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
              commentaire_responsable, id_demande))
        conn.commit()
        return self.get_by_id(id_demande)

    def delete(self, id_demande):
        conn = get_db()
        cursor = conn.execute("DELETE FROM demande_achat WHERE id_demande = ?",
                              (id_demande,))
        conn.commit()
        return cursor.rowcount