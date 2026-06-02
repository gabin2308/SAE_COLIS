from flask import Blueprint, request, jsonify
from app import limiter
from app.service.UtilisateurService import UtilisateurService
from app.controller.PermissionsController import reqrole
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from datetime import timedelta
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
        self.blueprint.add_url_rule('/change-password', view_func=self.change_password, methods=['POST'])

    # ─────────────────────────────────────────
    # CHANGEMENT DE MOT DE PASSE (SÉCURISÉ)
    # ─────────────────────────────────────────
    @jwt_required()
    def change_password(self):
        # Vérification du jeton spécifique pour le changement de mot de passe
        claims = get_jwt()
        if claims.get("action") != "change_password":
            return jsonify({"error": "Token invalide pour cette action"}), 403
        
        data = request.get_json(silent=True) or {}
        user_id = get_jwt_identity() # Identité extraite du token JWT
        new_password = data.get('new_password')

        if not new_password:
            return jsonify({"error": "Nouveau mot de passe requis"}), 400

        try:
            self.us.update_password(user_id, new_password)
            return jsonify({"message": "Mot de passe mis à jour avec succès"}), 200
        except Exception as e:
            logging.error(f"Erreur changement mot de passe: {e}")
            return jsonify({"error": "Erreur lors de la mise à jour"}), 500

    # ─────────────────────────────────────────
    # LOGIN
    # ─────────────────────────────────────────
    @limiter.limit("5 per minute; 20 per hour; 50 per day")
    def login(self):
        data = request.get_json(silent=True) or {}
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email et mot de passe requis"}), 400
        
        try:
            result = self.us.login(email, password)
            
            if not result.get("success"):
                return jsonify({"error": result.get("message")}), 401
            
            # Gestion du changement de mot de passe forcé avec token restreint (15 min)
            if result.get("must_change_password"):
                change_token = create_access_token(
                    identity=str(result["user"]["id_utilisateur"]),
                    expires_delta=timedelta(minutes=15),
                    additional_claims={"action": "change_password"}
                )
                return jsonify({
                    "message": "Changement de mot de passe requis",
                    "redirect": "/change-password",
                    "change_token": change_token,
                    "user_id": result["user"]["id_utilisateur"]
                }), 200

            # Connexion normale
            user = result["user"]
            token = create_access_token(identity=str(user["id_utilisateur"]), additional_claims={
                "role": user["role_nom"],
                "full_name": user["fullName"],
                "email": user["email"],
                "departement_id": user["departement_id"]
            })
            return jsonify({"message": "Connexion réussie", "access_token": token}), 200
        except Exception as e:
            logging.error(f"Erreur lors de la connexion: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500
        
    # ─────────────────────────────────────────
    # ADMINISTRATION
    # ─────────────────────────────────────────
    @reqrole('administrateur')
    def register(self):
        data = request.get_json(silent=True) or {}
        full_name = str(data.get('full_name', '')).strip()
        email = str(data.get('email', '')).strip()
        password = data.get('password')
        departement_id = data.get('departement_id')
        role_id = data.get('role_id')

        if not all([full_name, email, password, departement_id is not None, role_id is not None]):
            return jsonify({"error": "Tous les champs sont requis"}), 400

        try:
            user = self.us.create_user(full_name, email, password, role_id, departement_id)
            return jsonify({"message": "Utilisateur créé", "user_id": user.id_utilisateur}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement: {e}")
            return jsonify({"error": "Erreur serveur interne"}), 500
    
    @jwt_required()
    def logout(self):
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
            logging.error(f"Erreur lors de la récupération des informations: {e}")
            return jsonify({"error": "Impossible de récupérer les informations"}), 401

ctrl = UserController()