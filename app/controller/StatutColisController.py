from flask import Blueprint, request, jsonify
from app import limiter
from app.service.StatutColisService import StatutColisService
from app.controller.PermissionsController import login_required, reqrole
import logging

class StatutColisController:

    def __init__(self):
        self.blueprint = Blueprint('statut_colis', __name__)
        self.scs = StatutColisService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_statut>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_statut>', view_func=self.delete, methods=['DELETE'])

    @login_required
    def getAll(self):
        statuts = self.scs.get_all()
        return jsonify([s.to_dict() for s in statuts]), 200

    @login_required
    def getById(self, id_statut):
        try:
            statut = self.scs.get_by_id(id_statut)
            return jsonify(statut.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du statut {id_statut}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        libelle = data.get('libelle', '').strip()

        if not libelle:
            return jsonify({"error": "Le libellé est requis"}), 400

        try:
            statut = self.scs.create(libelle)
            return jsonify(statut.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            logging.error(f"Erreur lors de la création du statut: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur')
    @limiter.limit("10 per minute")
    def delete(self, id_statut):
        try:
            self.scs.delete(id_statut)
            return jsonify({"message": "Statut supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du statut {id_statut}: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

ctrl = StatutColisController()