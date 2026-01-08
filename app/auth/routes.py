from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Users
from ..extensions import db, blacklist
from . import auth_bp

# Route Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # ⬇⬇⬇  PENTING: identity DIKIRIM SEBAGAI DICT, BUKAN json.dumps(...)
        identity_payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
        access_token = create_access_token(identity=identity_payload)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401

# Route Logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"msg": "Logged out successfully"}), 200

# Route Register
@auth_bp.route('/register', methods=['POST'])
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

# Route GET login user
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current = get_jwt_identity()  # sekarang sudah DICT, tidak perlu json.loads
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
