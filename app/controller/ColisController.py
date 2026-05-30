from flask import Blueprint, request, jsonify, session
from app import limiter
from app.service.ColisService import ColisService
from app.controller.UserController import login_required, reqrole

class ColisController:

    def __init__(self):
        self.blueprint = Blueprint('colis', __name__)
        self.cs = ColisService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_colis>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/suivi/<string:numero_suivi>', view_func=self.getByNumeroSuivi, methods=['GET'])
        self.blueprint.add_url_rule('/mes-colis', view_func=self.getMesColis, methods=['GET'])
        self.blueprint.add_url_rule('/departement/<int:departement_id>', view_func=self.getByDepartement, methods=['GET'])
        self.blueprint.add_url_rule('/bon-commande/<int:bon_commande_id>', view_func=self.getByBonCommande, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_colis>/statut', view_func=self.updateStatut, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>/receptionner', view_func=self.receptionner, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>/retirer', view_func=self.retirer, methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>', view_func=self.update, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_colis>', view_func=self.delete, methods=['DELETE'])

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    def getAll(self):
        colis = self.cs.get_all()
        return jsonify([c.to_dict() for c in colis]), 200

    @login_required
    def getById(self, id_colis):
        try:
            colis = self.cs.get_by_id(id_colis)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    def getByNumeroSuivi(self, numero_suivi):
        try:
            colis = self.cs.get_by_numero_suivi(numero_suivi)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    def getMesColis(self):
        user_id = session.get('user_id')
        colis = self.cs.get_by_destinataire(user_id)
        return jsonify([c.to_dict() for c in colis]), 200

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ', 'directeur')
    def getByDepartement(self, departement_id):
        colis = self.cs.get_by_departement(departement_id)
        return jsonify([c.to_dict() for c in colis]), 200

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    def getByBonCommande(self, bon_commande_id):
        colis = self.cs.get_by_bon_commande(bon_commande_id)
        return jsonify([c.to_dict() for c in colis]), 200

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        bon_commande_id = data.get('bon_commande_id')
        statut_id = data.get('statut_id')

        if not bon_commande_id or not statut_id:
            return jsonify({"error": "bon_commande_id et statut_id requis"}), 400

        try:
            colis = self.cs.create(
                bon_commande_id=bon_commande_id,
                statut_id=statut_id,
                numero_suivi=data.get('numero_suivi'),
                code_barres=data.get('code_barres'),
                destinataire_id=data.get('destinataire_id'),
                commentaire=data.get('commentaire'),
                receptionne_par=data.get('receptionne_par')
            )
            return jsonify(colis.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def updateStatut(self, id_colis):
        data = request.get_json(force=True, silent=True) or {}
        statut_id = data.get('statut_id')

        if not statut_id:
            return jsonify({"error": "statut_id requis"}), 400

        try:
            colis = self.cs.update_statut(id_colis, statut_id)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def receptionner(self, id_colis):
        try:
            colis = self.cs.receptionner(id_colis, session.get('user_id'))
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def retirer(self, id_colis):
        try:
            colis = self.cs.retirer(id_colis)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def update(self, id_colis):
        data = request.get_json(force=True, silent=True) or {}
        try:
            colis = self.cs.update(id_colis, **data)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @login_required
    @reqrole('admin')
    @limiter.limit("10 per minute")
    def delete(self, id_colis):
        try:
            self.cs.delete(id_colis)
            return jsonify({"message": "Colis supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

ctrl = ColisController()