from flask import Blueprint, request, jsonify
from app import limiter
from app.service.UtilisateurService import UtilisateurService
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
import logging

class UserController:
    def __init__(self):
        self.blueprint = Blueprint('auth', __name__)
        self.us = UtilisateurService()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.blueprint.add_url_rule('/register', view_func=self.register, methods=['POST'])
        self.blueprint.add_url_rule('/logout', view_func=self.logout, methods=['POST'])
        self.blueprint.add_url_rule('/me', view_func=self.me, methods=['GET'])

    @limiter.limit("5 per minute; 20 per hour; 50 per day")
    def login(self):
        data = request.get_json(silent=True) or {}
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email et mot de passe requis"}), 400
        
        try:
            user = self.us.login(email, password)
            if not user:
                return jsonify({"error": "Identifiants incorrects"}), 401
            
            token = create_access_token(identity=str(user.id_utilisateur), additional_claims={
                "role": user.role_nom,
                "full_name": user.fullName,
                "email": user.email,
                "departement_id": user.departement_id
            })
            return jsonify({"message": "Connexion réussie", "access_token": token}), 200
        except Exception as e:
            logging.error(f"Erreur lors de la connexion: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500
        
    def register(self):
        data = request.get_json(silent=True) or {}
        full_name = str(data.get('full_name', '')).strip()
        email = str(data.get('email', '')).strip()
        password = data.get('password')
        departement_id = data.get('departement_id')
        role_id = 7  # lecteur par défaut

        if not all([full_name, email, password, departement_id is not None]):
            return jsonify({"error": "Tous les champs sont requis"}), 400

        try:
            user = self.us.create_user(full_name, email, password, role_id, departement_id)
            if not user:
                return jsonify({"error": "Erreur lors de la création de l'utilisateur"}), 400
            
            return jsonify({
                "message": "Utilisateur créé",
                "user_id": user.id_utilisateur
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500
    
    @jwt_required()
    def logout(self):
        # Note : Le JWT étant stateless, la révocation se gère idéalement via une blacklist/Redis
        return jsonify({"message": "Déconnexion effectuée"}), 200
    
    @jwt_required()
    def me(self):
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            return jsonify({
                "id": user_id,
                "full_name": claims.get("full_name"),
                "role": claims.get("role")
            }), 200
        except Exception as e:
            return jsonify({"error": "Impossible de récupérer les informations"}), 401

ctrl = UserController()