from flask import Blueprint, request, jsonify
from app import limiter
from app.service.DepartementService import DepartementService
from app.controller.PermissionsController import login_required, reqrole

class DepartementController:

    def __init__(self):
        self.blueprint = Blueprint('departement', __name__)
        self.ds = DepartementService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_departement>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_departement>', view_func=self.update, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_departement>', view_func=self.delete, methods=['DELETE'])
        self.blueprint.add_url_rule('/<int:id_departement>/budget', view_func=self.consommerBudget, methods=['PATCH'])

    
    def getAll(self):
        deps = self.ds.get_all()
        return jsonify([d.to_dict() for d in deps]), 200

    @login_required
    def getById(self, id_departement):
        try:
            dep = self.ds.get_by_id(id_departement)
            return jsonify(dep.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('administrateur')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        nom = data.get('nom', '').strip()
        telephone = data.get('telephone')
        budget_total = data.get('budget_total', 0)

        if not nom:
            return jsonify({"error": "Le nom est requis"}), 400

        try:
            dep = self.ds.create(nom, telephone, budget_total)
            return jsonify(dep.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409

    @login_required
    @reqrole('administrateur')
    @limiter.limit("30 per minute")
    def update(self, id_departement):
        data = request.get_json(force=True, silent=True) or {}

        try:
            dep = self.ds.update(
                id_departement,
                nom=data.get('nom'),
                telephone=data.get('telephone'),
                budget_total=data.get('budget_total')
            )
            return jsonify(dep.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('administrateur')
    @limiter.limit("30 per minute")
    def consommerBudget(self, id_departement):
        data = request.get_json(force=True, silent=True) or {}
        montant = data.get('montant')

        if montant is None:
            return jsonify({"error": "montant requis"}), 400

        try:
            dep = self.ds.consommer_budget(id_departement, montant)
            return jsonify(dep.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('administrateur')
    @limiter.limit("10 per minute")
    def delete(self, id_departement):
        try:
            self.ds.delete(id_departement)
            return jsonify({"message": "Département supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

ctrl = DepartementController()