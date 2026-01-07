from flask import request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from ..models import Users
from ..extensions import db
from . import users_bp

# Create User (Menambahkan User)
@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json

    # Validasi input untuk mencegah data kosong
    if not data.get('username') or not data.get('password') or not data.get('nama'):
        return jsonify({"msg": "Incomplete data"}), 400

    # Hash password yang diterima dari request
    hashed_password = generate_password_hash(data.get('password'))

    # Cek jika username sudah ada
    existing_user = Users.query.filter_by(username=data.get('username')).first()
    if existing_user:
        return jsonify({"msg": "Username already taken"}), 400

    # Buat user baru
    new_user = Users(
        username=data.get('username'),
        password=hashed_password,  # Password yang sudah di-hash
        nama=data.get('nama'),
        alamat=data.get('alamat'),
        telp=data.get('telp'),
        role=data.get('role', 'user')  # Default role adalah 'user' jika tidak diisi
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

# Read All Users (Mendapatkan Semua Users)
@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    users = Users.query.all()
    if not users:
        return jsonify({"msg": "No users found"}), 404
    
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "nama": user.nama,
            "alamat": user.alamat,
            "telp": user.telp,
            "role": user.role
        })
    return jsonify(result), 200

# Read Single User by ID (Mendapatkan User Berdasarkan ID)
@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = Users.query.get(id)

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

# Update User by ID (Mengupdate User Berdasarkan ID)
@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.json
    user = Users.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Validasi input
    if 'username' in data:
        # Cek jika username sudah ada untuk user lain
        existing_user = Users.query.filter_by(username=data.get('username')).first()
        if existing_user and existing_user.id != id:
            return jsonify({"msg": "Username already taken"}), 400
        user.username = data.get('username')

    # Jika ada password baru, hash password sebelum menyimpan
    if 'password' in data and data.get('password'):
        user.password = generate_password_hash(data.get('password'))

    # Update field lainnya
    user.nama = data.get('nama', user.nama)
    user.alamat = data.get('alamat', user.alamat)
    user.telp = data.get('telp', user.telp)
    user.role = data.get('role', user.role)

    db.session.commit()

    return jsonify({"msg": "User updated successfully"}), 200

# Delete User by ID (Menghapus User Berdasarkan ID)
@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = Users.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200
