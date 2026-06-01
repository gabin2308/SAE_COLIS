from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import limiter
from app.service.EvenementColisService import EvenementColisService
from app.controller.PermissionsController import login_required, reqrole
import logging

class EvenementColisController:

    def __init__(self):
        self.blueprint = Blueprint('evenement_colis', __name__)
        self.ecs = EvenementColisService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/colis/<int:colis_id>', view_func=self.getByColis, methods=['GET'])
        self.blueprint.add_url_rule('/colis/<int:colis_id>/dernier', view_func=self.getDernierEvenement, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_evenement>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/action/<string:action>', view_func=self.getByAction, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_evenement>', view_func=self.delete, methods=['DELETE'])

    @login_required
    def getByColis(self, colis_id):
        evenements = self.ecs.get_by_colis(colis_id)
        return jsonify([e.to_dict() for e in evenements]), 200

    @login_required
    def getDernierEvenement(self, colis_id):
        ev = self.ecs.get_dernier_evenement(colis_id)
        if not ev:
            return jsonify({"error": "Aucun événement pour ce colis"}), 404
        return jsonify(ev.to_dict()), 200

    @login_required
    def getById(self, id_evenement):
        try:
            ev = self.ecs.get_by_id(id_evenement)
            return jsonify(ev.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'événement {id_evenement}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur', 'agent_postal_iut', 'agent_postal_universite')
    def getByAction(self, action):
        try:
            evenements = self.ecs.get_by_action(action)
            return jsonify([e.to_dict() for e in evenements]), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'agent_postal_iut', 'agent_postal_universite')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        colis_id = data.get('colis_id')
        action = data.get('action')
        
        if not colis_id or not action:
            return jsonify({"error": "colis_id et action sont requis"}), 400
            
        try:
            ev = self.ecs.create(
                colis_id=colis_id,
                action=action,
                utilisateur_id=int(get_jwt_identity()),
                statut_libelle=data.get('statut_libelle'),
                commentaire=data.get('commentaire'),
                localisation=data.get('localisation'),
                transporteur=data.get('transporteur'),
                numero_livraison=data.get('numero_livraison'),
                date_expedition=data.get('date_expedition'),
                date_estimee_arrivee=data.get('date_estimee_arrivee')
            )
            return jsonify(ev.to_dict()), 201
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'événement: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur')
    @limiter.limit("10 per minute")
    def delete(self, id_evenement):
        try:
            self.ecs.delete(id_evenement)
            return jsonify({"message": "Événement supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'événement {id_evenement}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

ctrl = EvenementColisController()