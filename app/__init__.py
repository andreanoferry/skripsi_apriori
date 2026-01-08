import os
import json
from flask import Flask, jsonify
from .extensions import db, jwt, cors
from .auth import auth_bp
from .transactions import transactions_bp
from .strategies import strategies_bp
from .settings import settings_bp
from .users import users_bp
from .association import association_bp
from .config import Config
from .models import Transaction # Pastikan import Model Transaction ada

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi ekstensi
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # ========== JWT ERROR HANDLERS ==========
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"msg": "Missing or invalid Authorization header", "reason": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"msg": "Invalid token", "reason": reason}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token expired"}), 401

    # ========== REGISTER BLUEPRINTS (DENGAN PREFIX /api) ==========
    # Ini perbaikan utamanya: Tambah '/api' di depan
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(strategies_bp, url_prefix='/api/strategies')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(association_bp, url_prefix='/api/association')

    # ========== ROUTE SETUP DATABASE (HANYA SEKALI PAKAI) ==========
    @app.route('/setup-database-awal')
    def setup_database():
        try:
            with app.app_context():
                db.create_all()
            return "SUKSES! Tabel database berhasil dibuat."
        except Exception as e:
            return f"Gagal membuat database: {str(e)}"

    @app.route('/import-data-manual')
    def import_data():
        try:
            # Pastikan file json ada di folder app
            file_path = os.path.join(os.path.dirname(__file__), 'data_transaksi.json')
            
            if not os.path.exists(file_path):
                return "File 'data_transaksi.json' tidak ditemukan di folder app!"

            with open(file_path, 'r') as f:
                data_list = json.load(f)

            count = 0
            for item in data_list:
                # Periksa apakah data sudah ada (opsional) atau langsung masukkan
                # Sesuaikan nama kolom dengan JSON kamu
                new_trans = Transaction(
                    # CONTOH MAPPING (Ganti sesuai JSON & Model kamu):
                    # items_list=item['items'], 
                    # transaction_date=item['tanggal'],
                    # total_amount=item['total']
                )
                db.session.add(new_trans)
                count += 1
            
            db.session.commit()
            return f"Berhasil import {count} data transaksi!"
        except Exception as e:
            return f"Gagal import: {str(e)}"

    # ========== HEADER FIX ==========
    @app.after_request
    def skip_ngrok_warning(response):
        response.headers['ngrok-skip-browser-warning'] = 'any-value'
        return response

    return app