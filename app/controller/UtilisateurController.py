from flask import request, jsonify
from flask import Blueprint
from app import limiter
from app.controller.PermissionsController import reqrole,login_required
from app.service.UtilisateurService import UtilisateurService
from app import app
from flask_jwt_extended import create_access_token,get_jwt_identity, get_jwt,jwt_required

#Controller pour les utilisateurs

us = UtilisateurService()

class UserController:
    def __init__(self):

        self.blueprint = Blueprint('auth', __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.blueprint.add_url_rule('/register', view_func=self.register, methods=['POST'])
        self.blueprint.add_url_rule('/logout', view_func=self.logout, methods=['POST'])
        self.blueprint.add_url_rule('/me', view_func=self.me, methods=['GET'])


    #connexion avec limitation de 5 tentatives par minute, 20 par heure et 50 par jour pour éviter les attaques par force brute
    @limiter.limit("5 per minute; 20 per hour;50 per day")
    def login(self):

        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email et mot de passe requis"}), 400  
        
        user = us.login(email, password)
        if not user :
            return jsonify({"error": "Identifiants incorrects"}), 401
        token = create_access_token(identity=str(user.id_utilisateur), additional_claims={
            "role": user.role_nom,
            "full_name":user.fullName,
            "email":user.email,
            "departement_id":user.departement_id
        })
       
        return jsonify({"message": "Connexion réussie", "access_token": token})
        
    #creation d'un utilisateur local (non CAS) avec les champs requis : full_name, email, password et role_id. Le champ departement_id est optionnel.
    def register(self):

        data = request.get_json() or {}

        full_name = (data.get('full_name') or "").strip()
        email = (data.get('email')or "").strip()
        password = data.get('password')
        departement_id = data.get('departement_id')
        role_id = 7  # lecteur par défaut

        print(type(full_name), full_name)
        print(type(email), email)
        print(type(password), password)
        print(type(role_id), role_id)
        print(type(departement_id), departement_id)

        if not full_name or not email or not password or departement_id is None:
            return jsonify({"error": "Tous les champs sont requis"}), 400

        try:
            user = us.create_user(
                full_name,
                email,
                password,
                role_id,
                departement_id
            )
            if not user:
                return jsonify({"error": "Erreur lors de la création de l'utilisateur"}), 400
            
            return jsonify({
                "message": "Utilisateur créé",
                "user_id": user.id_utilisateur
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    
    @jwt_required()
    def logout(self):
        return jsonify({
            "message": "Déconnexion côté client (supprime le token)"
        }), 200
    
    @jwt_required()
    def me(self):
        user_id = get_jwt_identity()
        claims = get_jwt()

        return jsonify({
        "id": user_id,
        "full_name": claims.get("full_name"),
        "role": claims.get("role")
    }), 200

ctrl = UserController()