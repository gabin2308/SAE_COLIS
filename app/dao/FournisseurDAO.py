from app.database.initdb import get_db
from app.model.Fournisseur import Fournisseur
from app.model.Departement import Departement


# ═══════════════════════════════════════════════
# FOURNISSEUR DAO
# ═══════════════════════════════════════════════

class FournisseurDAO:

    def _base_select(self):
        return """
            SELECT f.*,
                   a.ville       AS adresse_ville,
                   a.rue         AS adresse_rue,
                   a.code_postal AS adresse_code_postal
            FROM fournisseur f
            LEFT JOIN adresse a ON a.id_adresse = f.adresse_id
        """

    def _fetch_one(self, where, params):
        conn = get_db()
        return conn.execute(self._base_select() + where, params).fetchone()

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        return conn.execute(self._base_select() + where, params).fetchall()

    # ── READ ──────────────────────────────────

    def get_all(self, actif_seulement=True):
        if actif_seulement:
            rows = self._fetch_all(" WHERE f.actif = 1")
        else:
            rows = self._fetch_all()
        return [Fournisseur(dict(r)) for r in rows]

    def get_by_id(self, id_fournisseur):
        row = self._fetch_one(" WHERE f.id_fournisseur = ?", (id_fournisseur,))
        return Fournisseur(dict(row)) if row else None

    def get_by_siret(self, siret):
        row = self._fetch_one(" WHERE f.siret = ?", (siret,))
        return Fournisseur(dict(row)) if row else None

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(
            " WHERE f.nom LIKE ? OR f.contact_email LIKE ? OR f.siret LIKE ?",
            (q, q, q)
        )
        return [Fournisseur(dict(r)) for r in rows]

    # ── CREATE ────────────────────────────────

    def create(self, nom, siret=None, site_web=None, contact_nom=None,
               contact_email=None, contact_telephone=None,
               delai_livraison_jours=None, conditions_paiement=None, adresse_id=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO fournisseur
                (nom, siret, site_web, contact_nom, contact_email,
                 contact_telephone, delai_livraison_jours, conditions_paiement, adresse_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, siret, site_web, contact_nom, contact_email,
              contact_telephone, delai_livraison_jours, conditions_paiement, adresse_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ── UPDATE ────────────────────────────────

    def update(self, id_fournisseur, nom=None, site_web=None, contact_nom=None,
               contact_email=None, contact_telephone=None,
               delai_livraison_jours=None, conditions_paiement=None):
        f = self.get_by_id(id_fournisseur)
        if not f:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE fournisseur SET
                nom = ?, site_web = ?, contact_nom = ?,
                contact_email = ?, contact_telephone = ?,
                delai_livraison_jours = ?, conditions_paiement = ?,
                date_modification = datetime('now')
            WHERE id_fournisseur = ?
        """, (
            nom                   or f.nom,
            site_web              or f.site_web,
            contact_nom           or f.contact_nom,
            contact_email         or f.contact_email,
            contact_telephone     or f.contact_telephone,
            delai_livraison_jours or f.delai_livraison_jours,
            conditions_paiement   or f.conditions_paiement,
            id_fournisseur
        ))
        conn.commit()
        return self.get_by_id(id_fournisseur)

    def desactiver(self, id_fournisseur):
        """Soft delete : désactive sans supprimer."""
        conn = get_db()
        conn.execute("""
            UPDATE fournisseur SET actif = 0, date_modification = datetime('now')
            WHERE id_fournisseur = ?
        """, (id_fournisseur,))
        conn.commit()
        return self.get_by_id(id_fournisseur)

    def reactiver(self, id_fournisseur):
        conn = get_db()
        conn.execute("""
            UPDATE fournisseur SET actif = 1, date_modification = datetime('now')
            WHERE id_fournisseur = ?
        """, (id_fournisseur,))
        conn.commit()
        return self.get_by_id(id_fournisseur)

    # ── DELETE ────────────────────────────────

    def delete(self, id_fournisseur):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM fournisseur WHERE id_fournisseur = ?", (id_fournisseur,)
        )
        conn.commit()
        return cursor.rowcount


# ═══════════════════════════════════════════════
# DEPARTEMENT DAO
# ═══════════════════════════════════════════════

class DepartementDAO:

    def _base_select(self):
        return """
            SELECT d.*,
                   a.ville       AS adresse_ville,
                   a.rue         AS adresse_rue,
                   a.code_postal AS adresse_code_postal
            FROM departement d
            LEFT JOIN adresse a ON a.id_adresse = d.adresse_id
        """

    def _fetch_one(self, where, params):
        conn = get_db()
        return conn.execute(self._base_select() + where, params).fetchone()

    def _fetch_all(self, where="", params=()):
        conn = get_db()
        return conn.execute(self._base_select() + where, params).fetchall()

    # ── READ ──────────────────────────────────

    def get_all(self):
        return [Departement(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_departement):
        row = self._fetch_one(" WHERE d.id_departement = ?", (id_departement,))
        return Departement(dict(row)) if row else None

    def get_by_nom(self, nom):
        row = self._fetch_one(" WHERE d.nom = ?", (nom,))
        return Departement(dict(row)) if row else None

    def search(self, query):
        q = f"%{query}%"
        rows = self._fetch_all(" WHERE d.nom LIKE ? OR d.email LIKE ?", (q, q))
        return [Departement(dict(r)) for r in rows]

    # ── CREATE ────────────────────────────────

    def create(self, nom, email, telephone=None, budget_total=0, adresse_id=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO departement (nom, email, telephone, budget_total, adresse_id)
            VALUES (?, ?, ?, ?, ?)
        """, (nom, email, telephone, budget_total, adresse_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    # ── UPDATE ────────────────────────────────

    def update(self, id_departement, nom=None, email=None, telephone=None, adresse_id=None):
        d = self.get_by_id(id_departement)
        if not d:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE departement SET nom = ?, email = ?, telephone = ?, adresse_id = ?
            WHERE id_departement = ?
        """, (
            nom        or d.nom,
            email      or d.email,
            telephone  or d.telephone,
            adresse_id or d.adresse_id,
            id_departement
        ))
        conn.commit()
        return self.get_by_id(id_departement)

    def update_budget(self, id_departement, budget_total=None, budget_utilise=None):
        d = self.get_by_id(id_departement)
        if not d:
            return None
        conn = get_db()
        conn.execute("""
            UPDATE departement SET budget_total = ?, budget_utilise = ?
            WHERE id_departement = ?
        """, (
            budget_total   if budget_total   is not None else d.budget_total,
            budget_utilise if budget_utilise is not None else d.budget_utilise,
            id_departement
        ))
        conn.commit()
        return self.get_by_id(id_departement)

    def consommer_budget(self, id_departement, montant):
        """Ajoute un montant au budget utilisé du département."""
        conn = get_db()
        conn.execute("""
            UPDATE departement
            SET budget_utilise = budget_utilise + ?
            WHERE id_departement = ?
        """, (montant, id_departement))
        conn.commit()
        return self.get_by_id(id_departement)

    # ── DELETE ────────────────────────────────

    def delete(self, id_departement):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM departement WHERE id_departement = ?", (id_departement,)
        )
        conn.commit()
        return cursor.rowcount