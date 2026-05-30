from flask import Blueprint, request, jsonify
from app import limiter
from app.service.FournisseurService import FournisseurService
from app.controller.UserController import login_required, reqrole

class FournisseurController:

    def __init__(self):
        self.blueprint = Blueprint('fournisseur', __name__)
        self.fs = FournisseurService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>', view_func=self.update, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>', view_func=self.delete, methods=['DELETE'])

    @login_required
    def getAll(self):
        fournisseurs = self.fs.get_all()
        return jsonify([f.to_dict() for f in fournisseurs]), 200

    @login_required
    def getById(self, id_fournisseur):
        try:
            f = self.fs.get_by_id(id_fournisseur)
            return jsonify(f.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'finance')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        nom = data.get('nom', '').strip()

        if not nom:
            return jsonify({"error": "Le nom est requis"}), 400

        try:
            f = self.fs.create(
                nom,
                contact_nom=data.get('contact_nom'),
                contact_email=data.get('contact_email'),
                contact_telephone=data.get('contact_telephone')
            )
            return jsonify(f.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409

    @login_required
    @reqrole('admin', 'finance')
    @limiter.limit("30 per minute")
    def update(self, id_fournisseur):
        data = request.get_json(force=True, silent=True) or {}
        try:
            f = self.fs.update(
                id_fournisseur,
                nom=data.get('nom'),
                contact_nom=data.get('contact_nom'),
                contact_email=data.get('contact_email'),
                contact_telephone=data.get('contact_telephone')
            )
            return jsonify(f.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin')
    @limiter.limit("10 per minute")
    def delete(self, id_fournisseur):
        try:
            self.fs.delete(id_fournisseur)
            return jsonify({"message": "Fournisseur supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

ctrl = FournisseurController()