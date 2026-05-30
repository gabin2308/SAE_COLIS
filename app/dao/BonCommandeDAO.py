from app.database.initdb import get_db
from app.model.BonCommande import BonCommande

class BonCommandeDAO:

    def _base_select(self):
        return """
            SELECT bc.*,
                d.nom AS departement_nom,
                f.nom AS fournisseur_nom,
                u.fullName AS createur_nom
            FROM bon_commande bc
            LEFT JOIN departement d ON bc.departement_id = d.id_departement
            LEFT JOIN fournisseur f ON bc.fournisseur_id = f.id_fournisseur
            LEFT JOIN utilisateur u ON bc.createur_id = u.id_utilisateur
        """

    def _fetch_one(self, where, params=()):
        conn = get_db()
        row = conn.execute(self._base_select() + where, params).fetchone()
        return BonCommande(dict(row)) if row else None

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        rows = conn.execute(self._base_select() + where, params).fetchall()
        return [BonCommande(dict(r)) for r in rows]

    def get_all(self):
        return self._fetch_all()

    def get_by_id(self, id_bon_commande):
        return self._fetch_one(" WHERE bc.id_bon_commande = ?", (id_bon_commande,))

    def get_by_numero(self, numero_commande):
        return self._fetch_one(" WHERE bc.numero_commande = ?", (numero_commande,))

    def get_by_departement(self, departement_id):
        return self._fetch_all(" WHERE bc.departement_id = ?", (departement_id,))

    def get_by_fournisseur(self, fournisseur_id):
        return self._fetch_all(" WHERE bc.fournisseur_id = ?", (fournisseur_id,))

    def get_by_createur(self, createur_id):
        return self._fetch_all(" WHERE bc.createur_id = ?", (createur_id,))

    def get_by_statut(self, statut):
        return self._fetch_all(" WHERE bc.statut = ?", (statut,))

    def create(self, numero_commande, date_commande, departement_id, fournisseur_id,
               createur_id, devis_id, date_estimee_livraison=None,
               montant_estime=0, commentaire=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO bon_commande (numero_commande, date_commande, date_estimee_livraison,
                montant_estime, statut, departement_id, fournisseur_id,
                createur_id, devis_id, commentaire)
            VALUES (?, ?, ?, ?, 'en_preparation', ?, ?, ?, ?, ?)
        """, (numero_commande, date_commande, date_estimee_livraison,
              montant_estime, departement_id, fournisseur_id,
              createur_id, devis_id, commentaire))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update_statut(self, id_bon_commande, statut):
        conn = get_db()
        conn.execute("UPDATE bon_commande SET statut = ? WHERE id_bon_commande = ?",
                     (statut, id_bon_commande))
        conn.commit()
        return self.get_by_id(id_bon_commande)

    def update(self, id_bon_commande, date_estimee_livraison=None,
               montant_estime=None, commentaire=None):
        bc = self.get_by_id(id_bon_commande)
        if not bc:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE bon_commande
            SET date_estimee_livraison = ?, montant_estime = ?, commentaire = ?
            WHERE id_bon_commande = ?
        """, (
            date_estimee_livraison or bc.date_estimee_livraison,
            montant_estime if montant_estime is not None else bc.montant_estime,
            commentaire or bc.commentaire,
            id_bon_commande
        ))
        conn.commit()
        return self.get_by_id(id_bon_commande)

    def delete(self, id_bon_commande):
        conn = get_db()
        cursor = conn.execute("DELETE FROM bon_commande WHERE id_bon_commande = ?",
                              (id_bon_commande,))
        conn.commit()
        return cursor.rowcount