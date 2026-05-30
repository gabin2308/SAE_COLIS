from flask import Blueprint, jsonify, session
from app.service.HistoriqueColisService import HistoriqueColisService
from app.controller.UserController import login_required, reqrole

class HistoriqueColisController:

    def __init__(self):
        self.blueprint = Blueprint('historique_colis', __name__)
        self.hs = HistoriqueColisService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/colis/<int:id_colis>', view_func=self.getByColis, methods=['GET'])
        self.blueprint.add_url_rule('/mes-actions', view_func=self.getMesActions, methods=['GET'])

    @login_required
    @reqrole('admin', 'postal_iut', 'postal_univ')
    def getByColis(self, id_colis):
        historique = self.hs.get_by_colis(id_colis)
        return jsonify([h.to_dict() for h in historique]), 200

    @login_required
    def getMesActions(self):
        historique = self.hs.get_by_utilisateur(session.get('user_id'))
        return jsonify([h.to_dict() for h in historique]), 200

ctrl = HistoriqueColisController()