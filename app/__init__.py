from flask import Flask
from .extensions import db, jwt, cors
from .auth import auth_bp
from .transactions import transactions_bp
from .strategies import strategies_bp
from .settings import settings_bp
from .users import users_bp
from .association import association_bp
from .config import Config

def create_app():
    app = Flask(__name__)
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

    # Tambahkan header untuk skip ngrok warning
    @app.after_request
    def skip_ngrok_warning(response):
        response.headers['ngrok-skip-browser-warning'] = 'any-value'
        return response

    return app
