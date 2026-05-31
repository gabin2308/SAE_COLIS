from flask import Blueprint, request, jsonify, session
from app import limiter
from app.service.DevisService import DevisService
from app.controller.UserController import login_required, reqrole

class DevisController:

    def __init__(self):
        self.blueprint = Blueprint('devis', __name__)
        self.ds = DevisService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/',                        view_func=self.getAll,           methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_devis>',          view_func=self.getById,          methods=['GET'])
        self.blueprint.add_url_rule('/fournisseur/<int:fournisseur_id>', view_func=self.getByFournisseur, methods=['GET'])
        self.blueprint.add_url_rule('/statut/<string:statut>',  view_func=self.getByStatut,      methods=['GET'])
        self.blueprint.add_url_rule('/',                        view_func=self.create,           methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_devis>',          view_func=self.update,           methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_devis>/accepter', view_func=self.accepter,         methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_devis>/refuser',  view_func=self.refuser,          methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_devis>',          view_func=self.delete,           methods=['DELETE'])

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    def getAll(self):
        devis = self.ds.get_all()
        return jsonify([d.to_dict() for d in devis]), 200

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    def getById(self, id_devis):
        try:
            devis = self.ds.get_by_id(id_devis)
            return jsonify(devis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    def getByFournisseur(self, fournisseur_id):
        devis = self.ds.get_by_fournisseur(fournisseur_id)
        return jsonify([d.to_dict() for d in devis]), 200

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    def getByStatut(self, statut):
        try:
            devis = self.ds.get_by_statut(statut)
            return jsonify([d.to_dict() for d in devis]), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'finance')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        fournisseur_id = data.get('fournisseur_id')
        createur_id    = session.get('user_id')

        if not fournisseur_id:
            return jsonify({"error": "fournisseur_id est requis"}), 400

        try:
            devis = self.ds.create(
                fournisseur_id=fournisseur_id,
                createur_id=createur_id,
                objet=data.get('objet'),
                montant_estime=data.get('montant_estime'),
                fichier_pdf=data.get('fichier_pdf')
            )
            return jsonify(devis.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'finance')
    @limiter.limit("30 per minute")
    def update(self, id_devis):
        data = request.get_json(force=True, silent=True) or {}
        try:
            devis = self.ds.update(id_devis, **data)
            return jsonify(devis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    @limiter.limit("30 per minute")
    def accepter(self, id_devis):
        try:
            devis = self.ds.accepter(id_devis)
            return jsonify(devis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    @limiter.limit("30 per minute")
    def refuser(self, id_devis):
        try:
            devis = self.ds.refuser(id_devis)
            return jsonify(devis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin')
    @limiter.limit("10 per minute")
    def delete(self, id_devis):
        try:
            self.ds.delete(id_devis)
            return jsonify({"message": "Devis supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

ctrl = DevisController()