from flask import request, jsonify, session, abort
from flask import Blueprint
from app.extensions import limiter
from functools import wraps
from app.service.UserService import UserService
from app import app

# Les décorateurs d'authentification et d'autorisation

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        return jsonify({"error": "Connectez-vous pour accéder à cette page"}), 401
    return wrap



def reqrole(*roles):
    def wrap(f):
        @wraps(f)
        def verifyRole(*args, **kwargs):
            if not session.get('logged'):
                return jsonify({"error": "Non connecté"}), 401
            if session.get('role') not in roles:
                return jsonify({"error": "Accès interdit"}), 403
            return f(*args, **kwargs)
        return verifyRole
    return wrap


#Controller pour les utilisateurs

us = UserService()

class UserController:
    def __init__(self):

        self.blueprint = Blueprint('auth', __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/login', view_function=self.login, methods=['POST'])
        self.blueprint.add_url_rule('/register', view_function=self.register, methods=['POST'])
        self.blueprint.add_url_rule('/logout', view_function=self.logout, methods=['POST'])


    #connexion avec limitation de 5 tentatives par minute, 20 par heure et 50 par jour pour éviter les attaques par force brute
    @limiter.limit("5 per minute; 20 per hour;50 per day")
    def login(self):

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email et mot de passe requis"}), 400  
        
        user = us.login(email, password)
        if user:
            session['logged'] = True
            session['user_id'] = user.id_utilisateur
            session['role'] = user.role_libelle
            return jsonify({"message": "Connexion réussie"})
        else:
            return jsonify({"error": "Email ou mot de passe incorrect"}), 401
        
    #creation d'un utilisateur local (non CAS) avec les champs requis : full_name, email, password et role_id. Le champ departement_id est optionnel.
    def register(self):

        data = request.get_json() or {}
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id')

        if not all([full_name, email, password, role_id]):
            return jsonify({"error": "Tous les champs sont requis"}), 400
        
        user = us.create_user(full_name, email, password, role_id)
        if user:
            return jsonify({"message": "Utilisateur créé"}), 201
        else:
            return jsonify({"error": "Erreur lors de la création de l'utilisateur"}), 500
        

    def logout(self):
        session.clear()
        return jsonify({"success": True, "message": "Déconnecté"})
