from flask import Blueprint, request, jsonify, session
from app import limiter
from app.service.DemandeAchatService import DemandeAchatService
from app.controller.UserController import login_required, reqrole

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

    @login_required
    @reqrole('admin', 'directeur', 'finance')
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
        demandes = self.das.get_by_demandeur(session.get('user_id'))
        return jsonify([d.to_dict() for d in demandes]), 200

    @login_required
    @reqrole('admin', 'directeur', 'finance')
    def getByDepartement(self, departement_id):
        demandes = self.das.get_by_departement(departement_id)
        return jsonify([d.to_dict() for d in demandes]), 200

    @login_required
    @reqrole('admin', 'directeur')
    def getEnAttente(self, departement_id):
        demandes = self.das.get_en_attente_departement(departement_id)
        return jsonify([d.to_dict() for d in demandes]), 200

    @login_required
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        objet = data.get('objet', '').strip()

        if not objet:
            return jsonify({"error": "L'objet est requis"}), 400

        try:
            demande = self.das.create(
                objet=objet,
                demandeur_id=session.get('user_id'),
                departement_id=session.get('departement_id'),
                description=data.get('description'),
                montant_estime=data.get('montant_estime')
            )
            return jsonify(demande.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'directeur')
    @limiter.limit("30 per minute")
    def approuver(self, id_demande):
        data = request.get_json(force=True, silent=True) or {}
        try:
            demande = self.das.approuver(id_demande, data.get('commentaire'))
            return jsonify(demande.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'directeur')
    @limiter.limit("30 per minute")
    def refuser(self, id_demande):
        data = request.get_json(force=True, silent=True) or {}
        try:
            demande = self.das.refuser(id_demande, data.get('commentaire'))
            return jsonify(demande.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @limiter.limit("10 per minute")
    def delete(self, id_demande):
        try:
            self.das.delete(id_demande)
            return jsonify({"message": "Demande supprimée"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

ctrl = DemandeAchatController()