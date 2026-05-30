from app.database.initdb import get_db
from app.model.Notification import Notification

class NotificationDAO:

    def get_by_utilisateur(self, id_utilisateur):
        conn = get_db()
        rows = conn.execute("""
            SELECT * FROM notification
            WHERE id_utilisateur = ?
            ORDER BY date_envoi DESC
        """, (id_utilisateur,)).fetchall()
        return [Notification(dict(r)) for r in rows]

    def get_non_lues(self, id_utilisateur):
        conn = get_db()
        rows = conn.execute("""
            SELECT * FROM notification
            WHERE id_utilisateur = ? AND lu = 0
            ORDER BY date_envoi DESC
        """, (id_utilisateur,)).fetchall()
        return [Notification(dict(r)) for r in rows]

    def get_by_id(self, id_notification):
        conn = get_db()
        row = conn.execute("SELECT * FROM notification WHERE id_notification = ?",
                           (id_notification,)).fetchone()
        return Notification(dict(row)) if row else None

    def create(self, id_utilisateur, message):
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO notification (id_utilisateur, message_notification)
            VALUES (?, ?)
        """, (id_utilisateur, message))
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def marquer_lu(self, id_notification):
        conn = get_db()
        conn.execute("UPDATE notification SET lu = 1 WHERE id_notification = ?",
                     (id_notification,))
        conn.commit()
        return self.get_by_id(id_notification)

    def marquer_toutes_lues(self, id_utilisateur):
        conn = get_db()
        conn.execute("UPDATE notification SET lu = 1 WHERE id_utilisateur = ?",
                     (id_utilisateur,))
        conn.commit()

    def delete(self, id_notification):
        conn = get_db()
        cursor = conn.execute("DELETE FROM notification WHERE id_notification = ?",
                              (id_notification,))
        conn.commit()
        return cursor.rowcount

    def delete_toutes(self, id_utilisateur):
        conn = get_db()
        cursor = conn.execute("DELETE FROM notification WHERE id_utilisateur = ?",
                              (id_utilisateur,))
        conn.commit()
        return cursor.rowcount