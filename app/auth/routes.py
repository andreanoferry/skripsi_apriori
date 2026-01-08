from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Users
from ..extensions import db, blacklist
from . import auth_bp

# ==========================================
# 1. ROUTE LOGIN
# ==========================================
# strict_slashes=False -> Mencegah Error 405 jika ada slash berlebih
@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        identity_payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
        access_token = create_access_token(identity=identity_payload)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401

# ==========================================
# 2. ROUTE LOGOUT
# ==========================================
@auth_bp.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"msg": "Logged out successfully"}), 200

# ==========================================
# 3. ROUTE REGISTER
# ==========================================
@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    data = request.json or {}

    if not data.get('username') or not data.get('password') or not data.get('nama'):
        return jsonify({"msg": "Incomplete data"}), 400

    hashed_password = generate_password_hash(data.get('password'))
    existing_user = Users.query.filter_by(username=data.get('username')).first()
    if existing_user:
        return jsonify({"msg": "Username already taken"}), 400

    new_user = Users(
        username=data.get('username'),
        password=hashed_password,
        nama=data.get('nama'),
        alamat=data.get('alamat'),
        telp=data.get('telp'),
        role=data.get('role')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

# ==========================================
# 4. ROUTE CEK USER (ME)
# ==========================================
@auth_bp.route('/me', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_current_user():
    current = get_jwt_identity()
    user = Users.query.filter_by(username=current["username"]).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "nama": user.nama,
        "alamat": user.alamat,
        "telp": user.telp,
        "role": user.role
    }), 200

# ==========================================
# 5. ROUTE DARURAT (RESET ADMIN)
# ==========================================
# Akses ini lewat browser untuk memperbaiki "Incorrect Password"
@auth_bp.route('/reset-admin-paksa', methods=['GET'], strict_slashes=False)
def reset_admin_paksa():
    try:
        # Hapus admin lama biar bersih
        target_user = "admin1"
        existing = Users.query.filter_by(username=target_user).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
        
        # Buat admin baru. Password: 123
        # Enkripsi dilakukan langsung di server Railway agar valid
        new_admin = Users(
            username=target_user,
            password=generate_password_hash("123"), 
            nama="Admin Reset",
            alamat="Server Railway",
            telp="08123456",
            role="admin"
        )
        db.session.add(new_admin)
        db.session.commit()
        
        return jsonify({"msg": f"SUKSES! User '{target_user}' dibuat. Password: '123'"}), 200
    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500