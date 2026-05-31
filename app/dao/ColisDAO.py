from app.database.initdb import get_db
from app.model.Colis import Colis


class ColisDAO:

    def _base_select(self):
        return """
            SELECT c.*,
                   s.libelle       AS statut_libelle,
                   u.fullName      AS destinataire_nom,
                   ag.fullName     AS receptionne_par_nom,
                   bc.numero_commande
            FROM colis c
            JOIN statut_colis  s  ON s.id_statut        = c.statut_id
            JOIN bon_commande  bc ON bc.id_bon_commande  = c.bon_commande_id
            LEFT JOIN utilisateur u  ON u.id_utilisateur = c.destinataire_id
            LEFT JOIN utilisateur ag ON ag.id_utilisateur = c.receptionne_par
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
        return [Colis(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_colis):
        row = self._fetch_one(" WHERE c.id_colis = ?", (id_colis,))
        return Colis(dict(row)) if row else None

    def get_by_numero_suivi(self, numero_suivi):
        row = self._fetch_one(" WHERE c.numero_suivi = ?", (numero_suivi,))
        return Colis(dict(row)) if row else None

    def get_by_qr_payload(self, qr_payload):
        """Recherche rapide après scan QR code."""
        row = self._fetch_one(" WHERE c.qr_payload = ?", (qr_payload,))
        return Colis(dict(row)) if row else None

    def get_by_bon_commande(self, bon_commande_id):
        rows = self._fetch_all(" WHERE c.bon_commande_id = ?", (bon_commande_id,))
        return [Colis(dict(r)) for r in rows]

    def get_by_destinataire(self, destinataire_id):
        """Retourne tous les colis d'un destinataire."""
        rows = self._fetch_all(" WHERE c.destinataire_id = ?", (destinataire_id,))
        return [Colis(dict(r)) for r in rows]

    def get_by_statut(self, statut_libelle):
        """statut_libelle : 'recu_universite' | 'transfere_iut' | 'en_attente_retrait' | 'remis_destinataire' | 'incident'"""
        rows = self._fetch_all(" WHERE s.libelle = ?", (statut_libelle,))
        return [Colis(dict(r)) for r in rows]

    def get_en_attente_retrait(self):
        """Colis disponibles au bureau postal, non encore retirés."""
        rows = self._fetch_all(" WHERE s.libelle = 'en_attente_retrait'")
        return [Colis(dict(r)) for r in rows]

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(
            " WHERE c.numero_suivi LIKE ? OR c.code_barres LIKE ? OR u.fullName LIKE ?",
            (q, q, q)
        )
        return [Colis(dict(r)) for r in rows]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(self, bon_commande_id, numero_suivi, statut_libelle='recu_universite',
               destinataire_id=None, code_barres=None, commentaire=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO colis
                (bon_commande_id, numero_suivi, statut_id, destinataire_id, code_barres, commentaire)
            VALUES (
                ?, ?,
                (SELECT id_statut FROM statut_colis WHERE libelle = ?),
                ?, ?, ?
            )
        """, (bon_commande_id, numero_suivi, statut_libelle,
              destinataire_id, code_barres, commentaire))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ─────────────────────────────────────────
    # UPDATE STATUT
    # ─────────────────────────────────────────

    def _update_statut(self, id_colis, libelle):
        conn = get_db()
        conn.execute("""
            UPDATE colis
            SET statut_id = (SELECT id_statut FROM statut_colis WHERE libelle = ?)
            WHERE id_colis = ?
        """, (libelle, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    def receptionner(self, id_colis, agent_id):
        """Réceptionne un colis et enregistre l'agent et la date."""
        conn = get_db()
        conn.execute("""
            UPDATE colis
            SET statut_id = (SELECT id_statut FROM statut_colis WHERE libelle = 'en_attente_retrait'),
                date_reception = datetime('now'),
                receptionne_par = ?
            WHERE id_colis = ?
        """, (agent_id, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    def transferer_iut(self, id_colis):
        return self._update_statut(id_colis, 'transfere_iut')

    def remettre_destinataire(self, id_colis):
        """Marque le colis comme remis et enregistre la date de retrait."""
        conn = get_db()
        conn.execute("""
            UPDATE colis
            SET statut_id = (SELECT id_statut FROM statut_colis WHERE libelle = 'remis_destinataire'),
                date_retrait = datetime('now')
            WHERE id_colis = ?
        """, (id_colis,))
        conn.commit()
        return self.get_by_id(id_colis)

    def signaler_incident(self, id_colis, commentaire=None):
        conn = get_db()
        conn.execute("""
            UPDATE colis
            SET statut_id = (SELECT id_statut FROM statut_colis WHERE libelle = 'incident'),
                commentaire = ?
            WHERE id_colis = ?
        """, (commentaire, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    def update_qr(self, id_colis, qr_payload, qr_image_path):
        """Enregistre le QR code généré après l'insertion."""
        conn = get_db()
        conn.execute("""
            UPDATE colis SET qr_payload = ?, qr_image_path = ?
            WHERE id_colis = ?
        """, (qr_payload, qr_image_path, id_colis))
        conn.commit()
        return self.get_by_id(id_colis)

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_colis):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM colis WHERE id_colis = ?", (id_colis,)
        )
        conn.commit()
        return cursor.rowcount