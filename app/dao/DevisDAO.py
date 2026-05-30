from app.database.initdb import get_db
from app.model.Devis import Devis

class DevisDAO:

    def _base_select(self):
        return """
            SELECT d.*,
                f.nom AS fournisseur_nom,
                u.fullName AS createur_nom
            FROM devis d
            LEFT JOIN fournisseur f ON d.fournisseur_id = f.id_fournisseur
            LEFT JOIN utilisateur u ON d.createur_id = u.id_utilisateur
        """

    def _fetch_one(self, where, params=()):
        conn = get_db()
        row = conn.execute(self._base_select() + where, params).fetchone()
        return Devis(dict(row)) if row else None

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        rows = conn.execute(self._base_select() + where, params).fetchall()
        return [Devis(dict(r)) for r in rows]

    def get_all(self):
        return self._fetch_all()

    def get_by_id(self, id_devis):
        return self._fetch_one(" WHERE d.id_devis = ?", (id_devis,))

    def get_by_fournisseur(self, fournisseur_id):
        return self._fetch_all(" WHERE d.fournisseur_id = ?", (fournisseur_id,))

    def get_by_createur(self, createur_id):
        return self._fetch_all(" WHERE d.createur_id = ?", (createur_id,))

    def get_by_statut(self, statut):
        return self._fetch_all(" WHERE d.statut = ?", (statut,))

    def create(self, date_demande, fournisseur_id, createur_id,
               objet=None, montant_estime=None, fichier_pdf=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO devis (date_demande, objet, montant_estime, fichier_pdf,
                               statut, fournisseur_id, createur_id)
            VALUES (?, ?, ?, ?, 'en_attente', ?, ?)
        """, (date_demande, objet, montant_estime, fichier_pdf,
              fournisseur_id, createur_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update_statut(self, id_devis, statut):
        conn = get_db()
        conn.execute("UPDATE devis SET statut = ? WHERE id_devis = ?", (statut, id_devis))
        conn.commit()
        return self.get_by_id(id_devis)

    def update(self, id_devis, objet=None, montant_estime=None, fichier_pdf=None, fournisseur_id=None):
        d = self.get_by_id(id_devis)
        if not d:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE devis
            SET objet = ?, montant_estime = ?, fichier_pdf = ?, fournisseur_id = ?
            WHERE id_devis = ?
        """, (
            objet or d.objet,
            montant_estime if montant_estime is not None else d.montant_estime,
            fichier_pdf or d.fichier_pdf,
            fournisseur_id or d.fournisseur_id,
            id_devis
        ))
        conn.commit()
        return self.get_by_id(id_devis)

    def delete(self, id_devis):
        conn = get_db()
        cursor = conn.execute("DELETE FROM devis WHERE id_devis = ?", (id_devis,))
        conn.commit()
        return cursor.rowcount