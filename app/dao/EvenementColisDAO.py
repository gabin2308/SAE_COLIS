from app.database.initdb import get_db
from app.model.EvenementColis import EvenementColis


class EvenementColisDAO:

    def _base_select(self):
        return """
            SELECT ec.*,
                   s.libelle      AS statut_libelle,
                   u.fullName     AS utilisateur_nom,
                   c.numero_suivi AS colis_numero_suivi
            FROM evenement_colis ec
            JOIN colis             c ON c.id_colis       = ec.colis_id
            LEFT JOIN statut_colis s ON s.id_statut      = ec.statut_id
            LEFT JOIN utilisateur  u ON u.id_utilisateur = ec.utilisateur_id
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
        return [EvenementColis(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_evenement):
        row = self._fetch_one(" WHERE ec.id = ?", (id_evenement,))
        return EvenementColis(dict(row)) if row else None

    def get_by_colis(self, colis_id):
        """Retourne tout l'historique d'un colis, trié du plus récent au plus ancien."""
        rows = self._fetch_all(
            " WHERE ec.colis_id = ? ORDER BY ec.date_evenement DESC",
            (colis_id,)
        )
        return [EvenementColis(dict(r)) for r in rows]

    def get_by_action(self, action):
        """action : 'scan_reception' | 'transfert_iut' | 'remise_destinataire' | 'incident'"""
        rows = self._fetch_all(" WHERE ec.action = ?", (action,))
        return [EvenementColis(dict(r)) for r in rows]

    def get_by_utilisateur(self, utilisateur_id):
        """Retourne tous les événements effectués par un agent."""
        rows = self._fetch_all(" WHERE ec.utilisateur_id = ?", (utilisateur_id,))
        return [EvenementColis(dict(r)) for r in rows]

    def get_dernier_evenement(self, colis_id):
        """Retourne le dernier événement enregistré pour un colis."""
        row = self._fetch_one(
            " WHERE ec.colis_id = ? ORDER BY ec.date_evenement DESC LIMIT 1",
            (colis_id,)
        )
        return EvenementColis(dict(row)) if row else None

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(self, colis_id, action, utilisateur_id=None, statut_libelle=None,
               commentaire=None, localisation=None, transporteur=None,
               numero_livraison=None, date_expedition=None, date_estimee_arrivee=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO evenement_colis
                (colis_id, action, utilisateur_id, statut_id, commentaire,
                 localisation, transporteur, numero_livraison,
                 date_expedition, date_estimee_arrivee)
            VALUES (
                ?, ?, ?,
                (SELECT id_statut FROM statut_colis WHERE libelle = ?),
                ?, ?, ?, ?, ?, ?
            )
        """, (colis_id, action, utilisateur_id, statut_libelle,
              commentaire, localisation, transporteur,
              numero_livraison, date_expedition, date_estimee_arrivee))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_evenement):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM evenement_colis WHERE id = ?", (id_evenement,)
        )
        conn.commit()
        return cursor.rowcount