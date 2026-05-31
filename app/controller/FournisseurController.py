from flask import Blueprint, request, jsonify
from app import limiter
from app.service.FournisseurService import FournisseurService
from app.controller.PermissionsController import login_required, reqrole


class FournisseurController:

    def __init__(self):
        self.blueprint = Blueprint('fournisseur', __name__)
        self.fs = FournisseurService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/',                                    view_func=self.getAll,      methods=['GET'])
        self.blueprint.add_url_rule('/search',                              view_func=self.search,      methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>',                view_func=self.getById,     methods=['GET'])
        self.blueprint.add_url_rule('/',                                    view_func=self.create,      methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>',                view_func=self.update,      methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>/desactiver',     view_func=self.desactiver,  methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>/reactiver',      view_func=self.reactiver,   methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_fournisseur>',                view_func=self.delete,      methods=['DELETE'])

    @login_required
    def getAll(self):
        actif_seulement = request.args.get('actif', 'true').lower() != 'false'
        fournisseurs = self.fs.get_all(actif_seulement)
        return jsonify([f.to_dict() for f in fournisseurs]), 200

    @login_required
    def search(self):
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({"error": "Paramètre q requis"}), 400
        return jsonify([f.to_dict() for f in self.fs.search(query)]), 200

    @login_required
    def getById(self, id_fournisseur):
        try:
            f = self.fs.get_by_id(id_fournisseur)
            return jsonify(f.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'responsable_financier')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        nom = data.get('nom', '').strip()
        if not nom:
            return jsonify({"error": "Le nom est requis"}), 400
        try:
            f = self.fs.create(
                nom=nom,
                siret=data.get('siret'),
                site_web=data.get('site_web'),
                contact_nom=data.get('contact_nom'),
                contact_email=data.get('contact_email'),
                contact_telephone=data.get('contact_telephone'),
                delai_livraison_jours=data.get('delai_livraison_jours'),
                conditions_paiement=data.get('conditions_paiement')
            )
            return jsonify(f.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409

    @reqrole('administrateur', 'responsable_financier')
    @limiter.limit("30 per minute")
    def update(self, id_fournisseur):
        data = request.get_json(force=True, silent=True) or {}
        try:
            f = self.fs.update(
                id_fournisseur,
                nom=data.get('nom'),
                site_web=data.get('site_web'),
                contact_nom=data.get('contact_nom'),
                contact_email=data.get('contact_email'),
                contact_telephone=data.get('contact_telephone'),
                delai_livraison_jours=data.get('delai_livraison_jours'),
                conditions_paiement=data.get('conditions_paiement')
            )
            return jsonify(f.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'responsable_financier')
    @limiter.limit("30 per minute")
    def desactiver(self, id_fournisseur):
        try:
            f = self.fs.desactiver(id_fournisseur)
            return jsonify(f.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur')
    @limiter.limit("30 per minute")
    def reactiver(self, id_fournisseur):
        try:
            f = self.fs.reactiver(id_fournisseur)
            return jsonify(f.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur')
    @limiter.limit("10 per minute")
    def delete(self, id_fournisseur):
        try:
            self.fs.delete(id_fournisseur)
            return jsonify({"message": "Fournisseur supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404


ctrl = FournisseurController()