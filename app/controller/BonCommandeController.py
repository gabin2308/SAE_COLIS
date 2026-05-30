from flask import Blueprint, request, jsonify, session
from app import limiter
from app.service.BonCommandeService import BonCommandeService
from app.controller.UserController import login_required, reqrole

class BonCommandeController:

    def __init__(self):
        self.blueprint = Blueprint('bon_commande', __name__)
        self.bcs = BonCommandeService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/numero/<string:numero>', view_func=self.getByNumero, methods=['GET'])
        self.blueprint.add_url_rule('/mes-commandes', view_func=self.getMesCommandes, methods=['GET'])
        self.blueprint.add_url_rule('/departement/<int:departement_id>', view_func=self.getByDepartement, methods=['GET'])
        self.blueprint.add_url_rule('/statut/<string:statut>', view_func=self.getByStatut, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>', view_func=self.update, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>/statut', view_func=self.updateStatut, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_bon_commande>', view_func=self.delete, methods=['DELETE'])

    @login_required
    @reqrole('admin', 'finance', 'directeur', 'postal_iut', 'postal_univ')
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

    @login_required
    def getMesCommandes(self):
        bcs = self.bcs.get_by_createur(session.get('user_id'))
        return jsonify([bc.to_dict() for bc in bcs]), 200

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    def getByDepartement(self, departement_id):
        bcs = self.bcs.get_by_departement(departement_id)
        return jsonify([bc.to_dict() for bc in bcs]), 200

    @login_required
    @reqrole('admin', 'finance', 'directeur')
    def getByStatut(self, statut):
        try:
            bcs = self.bcs.get_by_statut(statut)
            return jsonify([bc.to_dict() for bc in bcs]), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'finance', 'departement')
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
                createur_id=session.get('user_id'),
                devis_id=data.get('devis_id'),
                date_estimee_livraison=data.get('date_estimee_livraison'),
                montant_estime=data.get('montant_estime', 0),
                commentaire=data.get('commentaire')
            )
            return jsonify(bc.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'finance')
    @limiter.limit("30 per minute")
    def update(self, id_bon_commande):
        data = request.get_json(force=True, silent=True) or {}
        try:
            bc = self.bcs.update(
                id_bon_commande,
                date_estimee_livraison=data.get('date_estimee_livraison'),
                montant_estime=data.get('montant_estime'),
                commentaire=data.get('commentaire')
            )
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'finance', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def updateStatut(self, id_bon_commande):
        data = request.get_json(force=True, silent=True) or {}
        statut = data.get('statut')

        if not statut:
            return jsonify({"error": "statut requis"}), 400

        try:
            bc = self.bcs.update_statut(id_bon_commande, statut)
            return jsonify(bc.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin')
    @limiter.limit("10 per minute")
    def delete(self, id_bon_commande):
        try:
            self.bcs.delete(id_bon_commande)
            return jsonify({"message": "Bon de commande supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

ctrl = BonCommandeController()