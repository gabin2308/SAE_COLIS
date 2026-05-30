from flask import Blueprint, request, jsonify, session
from app import limiter
from app.service.UserService import UserService
from app.controller.UserController import login_required, reqrole

class AdminUserController:

    def __init__(self):
        self.blueprint = Blueprint('users', __name__)
        self.us = UserService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.getAll, methods=['GET'])
        self.blueprint.add_url_rule('/<int:id_utilisateur>', view_func=self.getById, methods=['GET'])
        self.blueprint.add_url_rule('/search', view_func=self.search, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/<int:id_utilisateur>', view_func=self.update, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_utilisateur>/password', view_func=self.updatePassword, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:id_utilisateur>', view_func=self.delete, methods=['DELETE'])

    @login_required
    @reqrole('admin')
    def getAll(self):
        users = self.us.get_all_users()
        return jsonify([u.to_dict() for u in users]), 200

    @login_required
    @reqrole('admin')
    def getById(self, id_utilisateur):
        user = self.us.get_user_by_id(id_utilisateur)
        if not user:
            return jsonify({"error": "Utilisateur introuvable"}), 404
        return jsonify(user.to_dict()), 200

    @login_required
    @reqrole('admin')
    def search(self):
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({"error": "Paramètre q requis"}), 400
        users = self.us.search_users(query)
        return jsonify([u.to_dict() for u in users]), 200

    @login_required
    @reqrole('admin')
    @limiter.limit("30 per minute")
    def create(self):
        data = request.get_json(force=True, silent=True) or {}
        full_name = data.get('full_name', '').strip()
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id')
        departement_id = data.get('departement_id')

        if not all([full_name, email, password, role_id, departement_id]):
            return jsonify({"error": "Tous les champs sont requis"}), 400

        try:
            user = self.us.create_user(full_name, email, password, role_id, departement_id)
            return jsonify(user.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @login_required
    @reqrole('admin')
    @limiter.limit("30 per minute")
    def update(self, id_utilisateur):
        data = request.get_json(force=True, silent=True) or {}

        try:
            user = self.us.update_user(
                id_utilisateur,
                full_name=data.get('full_name'),
                email=data.get('email'),
                role_id=data.get('role_id'),
                departement_id=data.get('departement_id')
            )
            if not user:
                return jsonify({"error": "Utilisateur introuvable"}), 404
            return jsonify(user.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @login_required
    @reqrole('admin')
    @limiter.limit("10 per minute")
    def updatePassword(self, id_utilisateur):
        data = request.get_json(force=True, silent=True) or {}
        new_password = data.get('password')

        if not new_password:
            return jsonify({"error": "Nouveau mot de passe requis"}), 400

        try:
            user = self.us.update_password(id_utilisateur, new_password)
            if not user:
                return jsonify({"error": "Utilisateur introuvable"}), 404
            return jsonify({"message": "Mot de passe mis à jour"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @login_required
    @reqrole('admin')
    @limiter.limit("10 per minute")
    def delete(self, id_utilisateur):
        # Empêche l'admin de se supprimer lui-même
        if session.get('user_id') == id_utilisateur:
            return jsonify({"error": "Impossible de supprimer votre propre compte"}), 403

        try:
            deleted = self.us.delete_user(id_utilisateur)
            if not deleted:
                return jsonify({"error": "Utilisateur introuvable"}), 404
            return jsonify({"message": "Utilisateur supprimé"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

ctrl = AdminUserController()