from app.database.initdb import get_db
from app.model.DemandeAchat import DemandeAchat


class DemandeAchatDAO:

    def _base_select(self):
        return """
            SELECT da.*,
                   u.fullName AS demandeur_nom,
                   d.nom      AS departement_nom
            FROM demande_achat da
            JOIN utilisateur  u ON u.id_utilisateur  = da.demandeur_id
            JOIN departement  d ON d.id_departement  = da.departement_id
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
        return [DemandeAchat(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_demande):
        row = self._fetch_one(" WHERE da.id_demande = ?", (id_demande,))
        return DemandeAchat(dict(row)) if row else None

    def get_by_demandeur(self, demandeur_id):
        """Retourne toutes les demandes d'un utilisateur (lecteur ou autre)."""
        rows = self._fetch_all(" WHERE da.demandeur_id = ?", (demandeur_id,))
        return [DemandeAchat(dict(r)) for r in rows]

    def get_by_departement(self, departement_id):
        """Retourne toutes les demandes d'un département (pour le responsable)."""
        rows = self._fetch_all(" WHERE da.departement_id = ?", (departement_id,))
        return [DemandeAchat(dict(r)) for r in rows]

    def get_by_statut(self, statut):
        """statut : 'en_attente' | 'approuvee' | 'refusee' | 'annulee'"""
        rows = self._fetch_all(" WHERE da.statut = ?", (statut,))
        return [DemandeAchat(dict(r)) for r in rows]

    def get_en_attente_par_departement(self, departement_id):
        """Demandes en attente pour un département donné (vue responsable)."""
        rows = self._fetch_all(
            " WHERE da.departement_id = ? AND da.statut = 'en_attente'",
            (departement_id,)
        )
        return [DemandeAchat(dict(r)) for r in rows]

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(
            " WHERE da.objet LIKE ? OR da.description LIKE ? OR u.fullName LIKE ?",
            (q, q, q)
        )
        return [DemandeAchat(dict(r)) for r in rows]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(self, objet, demandeur_id, departement_id, description=None, montant_estime=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO demande_achat (objet, description, montant_estime, demandeur_id, departement_id)
            VALUES (?, ?, ?, ?, ?)
        """, (objet, description, montant_estime, demandeur_id, departement_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def update(self, id_demande, objet=None, description=None, montant_estime=None):
        demande = self.get_by_id(id_demande)
        if not demande:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE demande_achat
            SET objet = ?, description = ?, montant_estime = ?
            WHERE id_demande = ?
        """, (
            objet          or demande.objet,
            description    or demande.description,
            montant_estime or demande.montant_estime,
            id_demande
        ))
        conn.commit()
        return self.get_by_id(id_demande)

    def approuver(self, id_demande, commentaire=None):
        conn = get_db()
        conn.execute("""
            UPDATE demande_achat
            SET statut = 'approuvee',
                date_traitement = datetime('now'),
                commentaire_responsable = ?
            WHERE id_demande = ?
        """, (commentaire, id_demande))
        conn.commit()
        return self.get_by_id(id_demande)

    def refuser(self, id_demande, commentaire=None):
        conn = get_db()
        conn.execute("""
            UPDATE demande_achat
            SET statut = 'refusee',
                date_traitement = datetime('now'),
                commentaire_responsable = ?
            WHERE id_demande = ?
        """, (commentaire, id_demande))
        conn.commit()
        return self.get_by_id(id_demande)

    def annuler(self, id_demande):
        conn = get_db()
        conn.execute("""
            UPDATE demande_achat
            SET statut = 'annulee', date_traitement = datetime('now')
            WHERE id_demande = ?
        """, (id_demande,))
        conn.commit()
        return self.get_by_id(id_demande)

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_demande):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM demande_achat WHERE id_demande = ?", (id_demande,)
        )
        conn.commit()
        return cursor.rowcount