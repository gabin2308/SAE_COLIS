from flask import Blueprint, request, jsonify, session
from app import limiter
from app.service.NotificationService import NotificationService
from app.controller.UserController import login_required, reqrole

class NotificationController:

    def __init__(self):
        self.blueprint = Blueprint('notification', __name__)
        self.ns = NotificationService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getMesNotifications, methods=['GET'])
        self.blueprint.add_url_rule('/non-lues', view_func=self.getNonLues, methods=['GET'])
        self.blueprint.add_url_rule('/count', view_func=self.compterNonLues, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_notification>/lire', view_func=self.marquerLu, methods=['PATCH'])
        self.blueprint.add_url_rule('/lire-toutes', view_func=self.marquerToutesLues, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_notification>', view_func=self.delete, methods=['DELETE'])
        self.blueprint.add_url_rule('/', view_func=self.deleteToutes, methods=['DELETE'])
        self.blueprint.add_url_rule('/envoyer', view_func=self.envoyer, methods=['POST'])

    @login_required
    def getMesNotifications(self):
        notifs = self.ns.get_by_utilisateur(session.get('user_id'))
        return jsonify([n.to_dict() for n in notifs]), 200

    @login_required
    def getNonLues(self):
        notifs = self.ns.get_non_lues(session.get('user_id'))
        return jsonify([n.to_dict() for n in notifs]), 200

    @login_required
    def compterNonLues(self):
        count = self.ns.compter_non_lues(session.get('user_id'))
        return jsonify({"count": count}), 200

    @login_required
    def marquerLu(self, id_notification):
        try:
            notif = self.ns.marquer_lu(id_notification)
            return jsonify(notif.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    def marquerToutesLues(self):
        self.ns.marquer_toutes_lues(session.get('user_id'))
        return jsonify({"message": "Toutes les notifications marquées comme lues"}), 200

    @login_required
    def delete(self, id_notification):
        try:
            self.ns.delete(id_notification)
            return jsonify({"message": "Notification supprimée"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    def deleteToutes(self):
        self.ns.delete_toutes(session.get('user_id'))
        return jsonify({"message": "Toutes les notifications supprimées"}), 200

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def envoyer(self):
        data = request.get_json(force=True, silent=True) or {}
        message = data.get('message')
        ids_utilisateurs = data.get('ids_utilisateurs', [])
        id_utilisateur = data.get('id_utilisateur')

        if not message:
            return jsonify({"error": "message requis"}), 400

        try:
            if ids_utilisateurs:
                self.ns.envoyer_multiple(ids_utilisateurs, message)
                return jsonify({"message": f"Notification envoyée à {len(ids_utilisateurs)} utilisateurs"}), 201
            elif id_utilisateur:
                notif = self.ns.envoyer(id_utilisateur, message)
                return jsonify(notif.to_dict()), 201
            else:
                return jsonify({"error": "id_utilisateur ou ids_utilisateurs requis"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

ctrl = NotificationController()