from app.database.initdb import get_db
from app.model.Devis import Devis


class DevisDAO:

    def _base_select(self):
        return """
            SELECT dv.*,
                   f.nom       AS fournisseur_nom,
                   u.fullName  AS createur_nom,
                   da.objet    AS demande_objet
            FROM devis dv
            JOIN fournisseur   f  ON f.id_fournisseur = dv.fournisseur_id
            JOIN utilisateur   u  ON u.id_utilisateur = dv.createur_id
            LEFT JOIN demande_achat da ON da.id_demande = dv.demande_id
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
        return [Devis(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_devis):
        row = self._fetch_one(" WHERE dv.id_devis = ?", (id_devis,))
        return Devis(dict(row)) if row else None

    def get_by_fournisseur(self, fournisseur_id):
        rows = self._fetch_all(" WHERE dv.fournisseur_id = ?", (fournisseur_id,))
        return [Devis(dict(r)) for r in rows]

    def get_by_demande(self, demande_id):
        rows = self._fetch_all(" WHERE dv.demande_id = ?", (demande_id,))
        return [Devis(dict(r)) for r in rows]

    def get_by_createur(self, createur_id):
        rows = self._fetch_all(" WHERE dv.createur_id = ?", (createur_id,))
        return [Devis(dict(r)) for r in rows]

    def get_by_statut(self, statut):
        """statut : 'en_attente' | 'accepte' | 'refuse'"""
        rows = self._fetch_all(" WHERE dv.statut = ?", (statut,))
        return [Devis(dict(r)) for r in rows]

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(
            " WHERE dv.objet LIKE ? OR f.nom LIKE ?",
            (q, q)
        )
        return [Devis(dict(r)) for r in rows]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(self, fournisseur_id, createur_id, objet=None,
               montant_estime=None, fichier_pdf=None, demande_id=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO devis (fournisseur_id, createur_id, objet, montant_estime, fichier_pdf, demande_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fournisseur_id, createur_id, objet, montant_estime, fichier_pdf, demande_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def update(self, id_devis, objet=None, montant_estime=None, fichier_pdf=None):
        devis = self.get_by_id(id_devis)
        if not devis:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE devis
            SET objet = ?, montant_estime = ?, fichier_pdf = ?
            WHERE id_devis = ?
        """, (
            objet          or devis.objet,
            montant_estime or devis.montant_estime,
            fichier_pdf    or devis.fichier_pdf,
            id_devis
        ))
        conn.commit()
        return self.get_by_id(id_devis)

    def accepter(self, id_devis):
        conn = get_db()
        conn.execute(
            "UPDATE devis SET statut = 'accepte' WHERE id_devis = ?",
            (id_devis,)
        )
        conn.commit()
        return self.get_by_id(id_devis)

    def refuser(self, id_devis):
        conn = get_db()
        conn.execute(
            "UPDATE devis SET statut = 'refuse' WHERE id_devis = ?",
            (id_devis,)
        )
        conn.commit()
        return self.get_by_id(id_devis)

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_devis):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM devis WHERE id_devis = ?", (id_devis,)
        )
        conn.commit()
        return cursor.rowcount