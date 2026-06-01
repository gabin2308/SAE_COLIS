from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import limiter
from app.service.NotificationService import NotificationService
from app.controller.PermissionsController import login_required, reqrole
import logging

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
        self.blueprint.add_url_rule('/tout-supprimer', view_func=self.deleteToutes, methods=['DELETE'])
        self.blueprint.add_url_rule('/envoyer', view_func=self.envoyer, methods=['POST'])

    @login_required
    def getMesNotifications(self):
        user_id = int(get_jwt_identity())
        notifs = self.ns.get_by_utilisateur(user_id)
        return jsonify([n.to_dict() for n in notifs]), 200

    @login_required
    def getNonLues(self):
        user_id = int(get_jwt_identity())
        notifs = self.ns.get_non_lues(user_id)
        return jsonify([n.to_dict() for n in notifs]), 200

    @login_required
    def compterNonLues(self):
        user_id = int(get_jwt_identity())
        count = self.ns.compter_non_lues(user_id)
        return jsonify({"count": count}), 200

    @login_required
    def marquerLu(self, id_notification):
        try:
            notif = self.ns.marquer_lu(id_notification)
            return jsonify(notif.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur marquage lu notification {id_notification}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @login_required
    def marquerToutesLues(self):
        user_id = int(get_jwt_identity())
        try:
            self.ns.marquer_toutes_lues(user_id)
            return jsonify({"message": "Toutes les notifications marquées comme lues"}), 200
        except Exception as e:
            logging.error(f"Erreur marquage toutes lues pour utilisateur {user_id}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @login_required
    def delete(self, id_notification):
        try:
            self.ns.delete(id_notification)
            return jsonify({"message": "Notification supprimée"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur suppression notification {id_notification}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @login_required
    def deleteToutes(self):
        user_id = int(get_jwt_identity())
        try:
            self.ns.delete_toutes(user_id)
            return jsonify({"message": "Toutes les notifications supprimées"}), 200
        except Exception as e:
            logging.error(f"Erreur suppression totale notifications pour {user_id}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur', 'agent_postal_iut', 'agent_postal_universite')
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
        except Exception as e:
            logging.error(f"Erreur envoi notification: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

ctrl = NotificationController()