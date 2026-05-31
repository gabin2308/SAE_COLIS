from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import limiter
from app.service.ColisService import ColisService
from app.controller.PermissionsController import login_required, reqrole


class ColisController:

    def __init__(self):
        self.blueprint = Blueprint('colis', __name__)
        self.cs = ColisService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/',                                        view_func=self.getAll,            methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_colis>',                          view_func=self.getById,           methods=['GET'])
        self.blueprint.add_url_rule('/suivi/<string:numero_suivi>',             view_func=self.getByNumeroSuivi,  methods=['GET'])
        self.blueprint.add_url_rule('/mes-colis',                               view_func=self.getMesColis,       methods=['GET'])
        self.blueprint.add_url_rule('/bon-commande/<int:bon_commande_id>',      view_func=self.getByBonCommande,  methods=['GET'])
        self.blueprint.add_url_rule('/',                                        view_func=self.create,            methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_colis>/receptionner',             view_func=self.receptionner,      methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>/retirer',                  view_func=self.retirer,           methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>/transferer',               view_func=self.transfererIut,     methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>/incident',                 view_func=self.signalerIncident,  methods=['PATCH'])
        self.blueprint.add_url_rule('/<int:id_colis>',                          view_func=self.update,            methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_colis>',                          view_func=self.delete,            methods=['DELETE'])
        self.blueprint.add_url_rule('/scan/<string:qr_payload>',
                             view_func=self.scanQR,
                             methods=['GET'])
    @reqrole('administrateur', 'postal_iut', 'postal_univ')
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
        user_id = int(get_jwt_identity())  # ✅ JWT
        colis = self.cs.get_by_destinataire(user_id)
        return jsonify([c.to_dict() for c in colis]), 200

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    def getByBonCommande(self, bon_commande_id):
        colis = self.cs.get_by_bon_commande(bon_commande_id)
        return jsonify([c.to_dict() for c in colis]), 200

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        bon_commande_id = data.get('bon_commande_id')
        if not bon_commande_id:
            return jsonify({"error": "bon_commande_id requis"}), 400
        try:
            colis = self.cs.create(
                bon_commande_id=bon_commande_id,
                numero_suivi=data.get('numero_suivi'),
                statut_libelle=data.get('statut_libelle', 'recu_universite'),  # ✅ string
                destinataire_id=data.get('destinataire_id'),
                code_barres=data.get('code_barres'),
                commentaire=data.get('commentaire')
            )
            return jsonify(colis.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def receptionner(self, id_colis):
        agent_id = int(get_jwt_identity())  # ✅ JWT
        try:
            colis = self.cs.receptionner(id_colis, agent_id)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def retirer(self, id_colis):
        try:
            colis = self.cs.retirer(id_colis)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def transfererIut(self, id_colis):
        try:
            colis = self.cs.transferer_iut(id_colis)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def signalerIncident(self, id_colis):
        data = request.get_json(force=True, silent=True) or {}
        try:
            colis = self.cs.signaler_incident(id_colis, data.get('commentaire'))
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur', 'postal_iut', 'postal_univ')
    @limiter.limit("30 per minute")
    def update(self, id_colis):
        data = request.get_json(force=True, silent=True) or {}
        try:
            colis = self.cs.update(id_colis, **data)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @reqrole('administrateur')
    @limiter.limit("10 per minute")
    def delete(self, id_colis):
        try:
            self.cs.delete(id_colis)
            return jsonify({"message": "Colis supprimé"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        
    @login_required
    def scanQR(self, qr_payload):
        try:
            colis = self.cs.get_by_qr_payload(qr_payload)
            return jsonify(colis.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

ctrl = ColisController()