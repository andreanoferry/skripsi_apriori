import os
from flask import Flask, send_from_directory, jsonify, request
from .extensions import db, jwt, cors
from .auth import auth_bp
from .transactions import transactions_bp
from .strategies import strategies_bp
from .settings import settings_bp
from .users import users_bp
from .association import association_bp
from .config import Config

def create_app():
    # 1. Tentukan lokasi folder 'dist' (Frontend Build)
    dist_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))

    # 2. Update Inisialisasi Flask
    app = Flask(__name__, static_folder=dist_folder, static_url_path='')
    
    app.config.from_object(Config)

    # ==========================================================
    # BAGIAN 1: SETTING CORS (AGAR TIDAK DIBLOKIR BROWSER)
    # ==========================================================
    # Kita izinkan semua origin (*)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # Inisialisasi database & JWT
    db.init_app(app)
    jwt.init_app(app)

    # ========== JWT ERROR HANDLERS (Agar Error Jelas) ==========
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"msg": "Missing or invalid Authorization header", "reason": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"msg": "Invalid token", "reason": reason}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token expired"}), 401

    # ==========================================================
    # BAGIAN 2: DAFTARKAN BLUEPRINT DENGAN PREFIX '/api'
    # ==========================================================
    # Ini memperbaiki Error 404/405 karena frontend menembak ke /api/...
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')         
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions') 
    app.register_blueprint(strategies_bp, url_prefix='/api/strategies')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(association_bp, url_prefix='/api/association')

    # Header tambahan untuk memastikan CORS benar-benar terbuka
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        return response

    # ========================================================
    # BAGIAN 3: SERVE FRONTEND (REACT/VUE)
    # ========================================================

    # Route Utama: Buka index.html
    @app.route('/')
    def serve():
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return "Folder 'dist' tidak ditemukan. Pastikan build frontend sukses!", 404

    # Error Handler 404: Handle Refresh Halaman Frontend
    @app.errorhandler(404)
    def not_found(e):
        # Jika request mengarah ke API tapi salah alamat, return JSON 404
        if request.path.startswith('/api'):
             return jsonify({"error": "API endpoint not found"}), 404
        
        # Jika bukan API, kembalikan ke index.html (untuk React Router)
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        return e

    return app