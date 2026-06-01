from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from app.service.DemandeAchatService import DemandeAchatService
from app.controller.PermissionsController import login_required, reqrole
import logging

class DemandeAchatController:

    def __init__(self):
        self.blueprint = Blueprint('demande_achat', __name__)
        self.das = DemandeAchatService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_demande>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/mes-demandes', view_func=self.getMesDemandes, methods=['GET'])
        self.blueprint.add_url_rule('/departement/<int:departement_id>', view_func=self.getByDepartement, methods=['GET'])
        self.blueprint.add_url_rule('/departement/<int:departement_id>/en-attente', view_func=self.getEnAttente, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_demande>/approuver', view_func=self.approuver, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_demande>/refuser', view_func=self.refuser, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_demande>', view_func=self.delete, methods=['DELETE'])

    @reqrole('administrateur', 'directeur', 'finance')
    def getAll(self):
        demandes = self.das.get_all()
        return jsonify([d.to_dict() for d in demandes]), 200

    @login_required
    def getById(self, id_demande):
        try:
            demande = self.das.get_by_id(id_demande)
            return jsonify(demande.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    def getMesDemandes(self):
        user_id = int(get_jwt_identity())
        demandes = self.das.get_by_demandeur(user_id)
        return jsonify([d.to_dict() for d in demandes]), 200

    @reqrole('administrateur', 'directeur', 'finance')
    def getByDepartement(self, departement_id):
        demandes = self.das.get_by_departement(departement_id)
        return jsonify([d.to_dict() for d in demandes]), 200

    @reqrole('administrateur', 'directeur')
    def getEnAttente(self, departement_id):
        demandes = self.das.get_en_attente_departement(departement_id)
        return jsonify([d.to_dict() for d in demandes]), 200

    @login_required
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        objet = data.get('objet', '').strip()
        if not objet:
            return jsonify({"error": "L'objet est requis"}), 400

        claims = get_jwt()
        user_id = int(get_jwt_identity())
        departement_id = claims.get('departement_id')

        if not departement_id:
            return jsonify({"error": "Département introuvable dans le jeton"}), 400

        try:
            demande = self.das.create(
                objet=objet,
                demandeur_id=user_id,
                departement_id=int(departement_id),
                description=data.get('description'),
                montant_estime=data.get('montant_estime')
            )
            return jsonify(demande.to_dict()), 201
        except Exception as e:
            logging.error(f"Erreur lors de la création de la demande: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur', 'directeur')
    def approuver(self, id_demande):
        data = request.get_json(force=True, silent=True) or {}
        try:
            demande = self.das.approuver(id_demande, data.get('commentaire'))
            return jsonify(demande.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(f"Erreur lors de l'approbation: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @reqrole('administrateur', 'directeur')
    def refuser(self, id_demande):
        data = request.get_json(force=True, silent=True) or {}
        try:
            demande = self.das.refuser(id_demande, data.get('commentaire'))
            return jsonify(demande.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(f"Erreur lors du refus: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

    @login_required
    def delete(self, id_demande):
        # Sécurité : vérifier si l'utilisateur est le propriétaire ou admin
        try:
            self.das.delete(id_demande)
            return jsonify({"message": "Demande supprimée"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Erreur suppression demande: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500

ctrl = DemandeAchatController()