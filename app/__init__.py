import os  # <--- WAJIB DITAMBAH
from flask import Flask, send_from_directory # <--- WAJIB DITAMBAH 'send_from_directory'
from .extensions import db, jwt, cors
from .auth import auth_bp
from .transactions import transactions_bp
from .strategies import strategies_bp
from .settings import settings_bp
from .users import users_bp
from .association import association_bp
from .config import Config

def create_app():
    # 1. Tentukan lokasi folder 'dist' (Relatif terhadap file __init__.py ini)
    # Artinya: Mundur satu folder (..), lalu cari folder 'dist'
    dist_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))

    # 2. Update Inisialisasi Flask agar membaca folder statis dari 'dist'
    app = Flask(__name__, static_folder=dist_folder, static_url_path='')
    
    app.config.from_object(Config)

    # Inisialisasi ekstensi
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # ========== JWT ERROR HANDLERS ==========
    from flask import jsonify

    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"msg": "Missing or invalid Authorization header", "reason": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"msg": "Invalid token", "reason": reason}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token expired"}), 401

    # Daftarkan blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(strategies_bp, url_prefix='/strategies')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(association_bp, url_prefix='/association')

    # Tambahkan header untuk skip ngrok warning (Opsional, boleh dihapus kalau gak pakai ngrok)
    @app.after_request
    def skip_ngrok_warning(response):
        response.headers['ngrok-skip-browser-warning'] = 'any-value'
        return response

    # ========================================================
    # TAMBAHAN KHUSUS UNTUK DEPLOY FRONTEND + BACKEND JADI 1
    # ========================================================

    # A. Route Utama: Menampilkan index.html saat web dibuka
    @app.route('/')
    def serve():
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return "Folder 'dist' belum ditemukan. Pastikan sudah jalankan 'npm run build'!", 404

    # B. Error Handler 404: Supaya React Router berfungsi saat di-refresh
    # Kalau user refresh di halaman /dashboard, Flask gak nemu route-nya, 
    # jadi kita paksa balikin index.html biar React yang handle.
    @app.errorhandler(404)
    def not_found(e):
        # Jika requestnya ke API (misal salah ketik URL API), biarkan return JSON 404
        # (Cek apakah URL mengandung salah satu prefix blueprint kamu)
        path = str(e.description) if hasattr(e, 'description') else ""
        # Atau cara gampang: cek request path
        from flask import request
        if request.path.startswith(('/auth', '/transactions', '/strategies', '/settings', '/users', '/association')):
             return jsonify({"error": "API endpoint not found"}), 404
        
        # Selain itu, kembalikan ke Frontend
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        return e

    return app