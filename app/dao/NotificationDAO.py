from app.database.initdb import get_db
from app.model.Notification import Notification


class NotificationDAO:

    def _base_select(self):
        return """
            SELECT n.*,
                   u.fullName AS utilisateur_nom
            FROM notification n
            JOIN utilisateur u ON u.id_utilisateur = n.id_utilisateur
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
        return [Notification(dict(r)) for r in self._fetch_all()]

    def get_by_id(self, id_notification):
        row = self._fetch_one(" WHERE n.id_notification = ?", (id_notification,))
        return Notification(dict(row)) if row else None

    def get_by_utilisateur(self, id_utilisateur):
        """Retourne toutes les notifications d'un utilisateur, les plus récentes en premier."""
        rows = self._fetch_all(
            " WHERE n.id_utilisateur = ? ORDER BY n.date_envoi DESC",
            (id_utilisateur,)
        )
        return [Notification(dict(r)) for r in rows]

    def get_non_lues(self, id_utilisateur):
        """Retourne les notifications non lues d'un utilisateur."""
        rows = self._fetch_all(
            " WHERE n.id_utilisateur = ? AND n.lu = 0 ORDER BY n.date_envoi DESC",
            (id_utilisateur,)
        )
        return [Notification(dict(r)) for r in rows]

    def count_non_lues(self, id_utilisateur):
        """Retourne le nombre de notifications non lues (pour le badge)."""
        conn = get_db()
        row = conn.execute("""
            SELECT COUNT(*) AS total
            FROM notification
            WHERE id_utilisateur = ? AND lu = 0
        """, (id_utilisateur,)).fetchone()
        return row['total'] if row else 0

    def get_by_type(self, id_utilisateur, type_notif):
        """type_notif : 'colis_recu' | 'colis_livre' | 'bc_valide' | etc."""
        rows = self._fetch_all(
            " WHERE n.id_utilisateur = ? AND n.type = ? ORDER BY n.date_envoi DESC",
            (id_utilisateur, type_notif)
        )
        return [Notification(dict(r)) for r in rows]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(self, id_utilisateur, message, type_notif=None, reference_id=None):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO notification (id_utilisateur, message, type, reference_id)
            VALUES (?, ?, ?, ?)
        """, (id_utilisateur, message, type_notif, reference_id))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def notifier_colis_recu(self, id_utilisateur, colis_id):
        return self.create(
            id_utilisateur,
            message="Votre colis est arrivé au bureau postal et est prêt à être retiré.",
            type_notif='colis_recu',
            reference_id=colis_id
        )

    def notifier_colis_livre(self, id_utilisateur, colis_id):
        return self.create(
            id_utilisateur,
            message="Votre colis vous a été remis.",
            type_notif='colis_livre',
            reference_id=colis_id
        )

    def notifier_bc_valide(self, id_utilisateur, bc_id):
        return self.create(
            id_utilisateur,
            message="Votre bon de commande a été validé par le responsable financier.",
            type_notif='bc_valide',
            reference_id=bc_id
        )

    def notifier_bc_refuse(self, id_utilisateur, bc_id):
        return self.create(
            id_utilisateur,
            message="Votre bon de commande a été refusé.",
            type_notif='bc_refuse',
            reference_id=bc_id
        )

    def notifier_devis_accepte(self, id_utilisateur, devis_id):
        return self.create(
            id_utilisateur,
            message="Votre devis a été accepté.",
            type_notif='devis_accepte',
            reference_id=devis_id
        )

    def notifier_devis_refuse(self, id_utilisateur, devis_id):
        return self.create(
            id_utilisateur,
            message="Votre devis a été refusé.",
            type_notif='devis_refuse',
            reference_id=devis_id
        )

    def notifier_demande_approuvee(self, id_utilisateur, demande_id):
        return self.create(
            id_utilisateur,
            message="Votre demande d'achat a été approuvée par votre responsable.",
            type_notif='autre',
            reference_id=demande_id
        )

    def notifier_demande_refusee(self, id_utilisateur, demande_id):
        return self.create(
            id_utilisateur,
            message="Votre demande d'achat a été refusée par votre responsable.",
            type_notif='autre',
            reference_id=demande_id
        )

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def marquer_lu(self, id_notification):
        conn = get_db()
        conn.execute(
            "UPDATE notification SET lu = 1 WHERE id_notification = ?",
            (id_notification,)
        )
        conn.commit()
        return self.get_by_id(id_notification)

    def marquer_toutes_lues(self, id_utilisateur):
        """Marque toutes les notifications d'un utilisateur comme lues."""
        conn = get_db()
        conn.execute(
            "UPDATE notification SET lu = 1 WHERE id_utilisateur = ?",
            (id_utilisateur,)
        )
        conn.commit()

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, id_notification):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM notification WHERE id_notification = ?", (id_notification,)
        )
        conn.commit()
        return cursor.rowcount

    def delete_all_by_utilisateur(self, id_utilisateur):
        conn = get_db()
        cursor = conn.execute(
            "DELETE FROM notification WHERE id_utilisateur = ?", (id_utilisateur,)
        )
        conn.commit()
        return cursor.rowcount