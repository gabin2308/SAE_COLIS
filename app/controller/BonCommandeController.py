from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from app import limiter
from app.service.BonCommandeService import BonCommandeService
from app.controller.PermissionsController import login_required, reqrole


class BonCommandeController:

    def __init__(self):
        self.blueprint = Blueprint('bon_commande', __name__)
        self.bcs = BonCommandeService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/',                                      view_func=self.getAll,          methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>',                 view_func=self.getById,         methods=['GET'])
        self.blueprint.add_url_rule('/numero/<string:numero>',                view_func=self.getByNumero,     methods=['GET'])
        self.blueprint.add_url_rule('/departement/<int:departement_id>',      view_func=self.getByDepartement,methods=['GET'])
        self.blueprint.add_url_rule('/statut/<string:statut>',                view_func=self.getByStatut,     methods=['GET'])
        self.blueprint.add_url_rule('/',                                      view_func=self.create,          methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>/commentaire',     view_func=self.updateCommentaire, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>/valider',         view_func=self.valider,         methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>/expedier',        view_func=self.expedier,        methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>/confirmer',       view_func=self.confirmerLivraison, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>/annuler',         view_func=self.annuler,         methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>',                 view_func=self.delete,          methods=['DELETE'])

    @reqrole('administrateur', 'responsable_financier', 'directeur', 'agent_postal_iut', 'agent_postal_universite')
    def getAll(self):
        bcs = self.bcs.get_all()
        return jsonify([bc.to_dict() for bc in bcs]), 200

    @login_required
    def getById(self, id_bon_commande):
        try:
            bc = self.bcs.get_by_id(id_bon_commande)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    def getByNumero(self, numero):
        try:
            bc = self.bcs.get_by_numero(numero)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'responsable_financier', 'directeur')
    def getByDepartement(self, departement_id):
        bcs = self.bcs.get_by_departement(departement_id)
        return jsonify([bc.to_dict() for bc in bcs]), 200

    @reqrole('administrateur', 'responsable_financier', 'directeur')
    def getByStatut(self, statut):
        try:
            bcs = self.bcs.get_by_statut(statut)
            return jsonify([bc.to_dict() for bc in bcs]), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'responsable_financier', 'responsable_departement')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        required = ['departement_id', 'fournisseur_id', 'devis_id']
        if not all(data.get(k) for k in required):
            return jsonify({"error": f"Champs requis : {required}"}), 400
        try:
            bc = self.bcs.create(
                departement_id=data.get('departement_id'),
                fournisseur_id=data.get('fournisseur_id'),
                createur_id=int(get_jwt_identity()),  # ✅ JWT
                devis_id=data.get('devis_id'),
                date_estimee_livraison=data.get('date_estimee_livraison'),
                montant_estime=data.get('montant_estime', 0),
                commentaire=data.get('commentaire')
            )
            return jsonify(bc.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'responsable_financier')
    @limiter.limit("30 per minute")
    def updateCommentaire(self, id_bon_commande):
        data = request.get_json(force=True, silent=True) or {}
        try:
            bc = self.bcs.update_commentaire(id_bon_commande, data.get('commentaire'))
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'responsable_financier')
    @limiter.limit("30 per minute")
    def valider(self, id_bon_commande):
        try:
            bc = self.bcs.valider(id_bon_commande)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'responsable_financier')
    @limiter.limit("30 per minute")
    def expedier(self, id_bon_commande):
        try:
            bc = self.bcs.expedier(id_bon_commande)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'agent_postal_iut', 'agent_postal_universite')
    @limiter.limit("30 per minute")
    def confirmerLivraison(self, id_bon_commande):
        try:
            bc = self.bcs.confirmer_livraison(id_bon_commande)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'responsable_financier', 'directeur')
    @limiter.limit("30 per minute")
    def annuler(self, id_bon_commande):
        try:
            bc = self.bcs.annuler(id_bon_commande)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur')
    @limiter.limit("10 per minute")
    def delete(self, id_bon_commande):
        try:
            self.bcs.delete(id_bon_commande)
            return jsonify({"message": "Bon de commande supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404


ctrl = BonCommandeController()