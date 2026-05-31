from app.database.initdb import get_db
from app.model.BonCommande import BonCommande


class BonCommandeDAO:

    def _base_select(self):
        return """
            SELECT bc.*,
                   s.libelle   AS statut_libelle,
                   d.nom       AS departement_nom,
                   f.nom       AS fournisseur_nom,
                   u.fullName  AS createur_nom
            FROM bon_commande bc
            JOIN statut_bon_commande s ON s.id_statut      = bc.statut_id
            JOIN departement         d ON d.id_departement = bc.departement_id
            JOIN fournisseur         f ON f.id_fournisseur = bc.fournisseur_id
            JOIN utilisateur         u ON u.id_utilisateur = bc.createur_id
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
        return [BonCommande(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_bon_commande):
        row = self._fetch_one(" WHERE bc.id_bon_commande = ?", (id_bon_commande,))
        return BonCommande(dict(row)) if row else None

    def get_by_numero(self, numero_commande):
        row = self._fetch_one(" WHERE bc.numero_commande = ?", (numero_commande,))
        return BonCommande(dict(row)) if row else None

    def get_by_departement(self, departement_id):
        rows = self._fetch_all(" WHERE bc.departement_id = ?", (departement_id,))
        return [BonCommande(dict(r)) for r in rows]

    def get_by_fournisseur(self, fournisseur_id):
        rows = self._fetch_all(" WHERE bc.fournisseur_id = ?", (fournisseur_id,))
        return [BonCommande(dict(r)) for r in rows]

    def get_by_statut(self, statut_libelle):
        """statut_libelle : 'en_preparation' | 'valide_finance' | 'expedie' | 'livre_confirme' | 'annule'"""
        rows = self._fetch_all(" WHERE s.libelle = ?", (statut_libelle,))
        return [BonCommande(dict(r)) for r in rows]

    def get_by_devis(self, devis_id):
        row = self._fetch_one(" WHERE bc.devis_id = ?", (devis_id,))
        return BonCommande(dict(row)) if row else None

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(
            " WHERE bc.numero_commande LIKE ? OR f.nom LIKE ? OR d.nom LIKE ?",
            (q, q, q)
        )
        return [BonCommande(dict(r)) for r in rows]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(self, numero_commande, departement_id, fournisseur_id,
               createur_id, devis_id, montant_estime=0,
               date_estimee_livraison=None, commentaire=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO bon_commande
                (numero_commande, departement_id, fournisseur_id, createur_id,
                 devis_id, montant_estime, date_estimee_livraison, commentaire)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (numero_commande, departement_id, fournisseur_id, createur_id,
              devis_id, montant_estime, date_estimee_livraison, commentaire))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ─────────────────────────────────────────
    # UPDATE STATUT
    # ─────────────────────────────────────────

    def _update_statut(self, id_bon_commande, libelle):
        conn = get_db()
        conn.execute("""
            UPDATE bon_commande
            SET statut_id = (SELECT id_statut FROM statut_bon_commande WHERE libelle = ?)
            WHERE id_bon_commande = ?
        """, (libelle, id_bon_commande))
        conn.commit()
        return self.get_by_id(id_bon_commande)

    def valider(self, id_bon_commande):
        return self._update_statut(id_bon_commande, 'valide_finance')

    def expedier(self, id_bon_commande):
        return self._update_statut(id_bon_commande, 'expedie')

    def confirmer_livraison(self, id_bon_commande):
        return self._update_statut(id_bon_commande, 'livre_confirme')

    def annuler(self, id_bon_commande):
        return self._update_statut(id_bon_commande, 'annule')

    def update_commentaire(self, id_bon_commande, commentaire):
        conn = get_db()
        conn.execute(
            "UPDATE bon_commande SET commentaire = ? WHERE id_bon_commande = ?",
            (commentaire, id_bon_commande)
        )
        conn.commit()
        return self.get_by_id(id_bon_commande)

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_bon_commande):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM bon_commande WHERE id_bon_commande = ?", (id_bon_commande,)
        )
        conn.commit()
        return cursor.rowcount