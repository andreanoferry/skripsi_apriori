from flask import request, jsonify
from ..models import Strategies
from ..extensions import db
from . import strategies_bp
from flask_jwt_extended import jwt_required

# Create Strategy (Menambahkan Strategy)
@strategies_bp.route('/', methods=['POST'])
@jwt_required()
def create_strategy():
    data = request.json

    # Validasi input yang diperlukan
    if not data.get('nama') or not data.get('keterangan') or not data.get('status'):
        return jsonify({"msg": "Incomplete data"}), 400
    
    if data.get('status') not in ['active', 'non active']:
        return jsonify({"msg": "Status must be 'active' or 'non active'"}), 400

    # Buat strategy baru
    new_strategy = Strategies(
        nama=data.get('nama'),
        keterangan=data.get('keterangan'),
        status=data.get('status')
    )
    db.session.add(new_strategy)
    db.session.commit()

    return jsonify({"msg": "Strategy created successfully", "strategy": {
        "id": new_strategy.id,
        "nama": new_strategy.nama,
        "keterangan": new_strategy.keterangan,
        "status": new_strategy.status
    }}), 201

# Read All Strategies (Mendapatkan Semua Strategies)
@strategies_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_strategies():
    strategies = Strategies.query.all()
    if not strategies:
        return jsonify({"msg": "No strategies found"}), 404
    
    result = []
    for strategy in strategies:
        result.append({
            "id": strategy.id,
            "nama": strategy.nama,
            "keterangan": strategy.keterangan,
            "status": strategy.status
        })
    return jsonify(result), 200


# Read Active Strategies (✅ KINI MENGEMBALIKAN ARRAY)
@strategies_bp.route('/active', methods=['GET'])
@jwt_required()
def get_active_strategies():
    # Ambil SEMUA strategy yang berstatus 'active'
    rows = Strategies.query.filter_by(status='active').all()
    if not rows:
        return jsonify([]), 200  # kembalikan array kosong agar frontend aman

    result = [{
        "id": s.id,
        "nama": s.nama,
        "keterangan": s.keterangan,
        "status": s.status
    } for s in rows]

    return jsonify(result), 200

# Update Status Strategy (✅ TIDAK LAGI MENONAKTIFKAN STRATEGI LAIN)
@strategies_bp.route('/status/<int:id>', methods=['PUT'])
@jwt_required()
def update_strategy_status(id):
    data = request.json
    new_status = data.get('status')

    if new_status not in ['active', 'non active']:
        return jsonify({"msg": "Invalid status. Status must be 'active' or 'non active'"}), 400

    strategy = Strategies.query.get(id)
    if not strategy:
        return jsonify({"msg": "Strategy not found"}), 404

    # HANYA update strategy ini saja — strategi lain tetap seperti sedia kala
    strategy.status = new_status
    db.session.commit()

    return jsonify({
        "msg": f"Strategy {id} updated to {new_status} successfully",
        "id": strategy.id,
        "nama": strategy.nama,
        "keterangan": strategy.keterangan,
        "status": strategy.status
    }), 200

# Update Strategy by ID (Mengupdate Strategy Berdasarkan ID)
@strategies_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_strategy(id):
    data = request.json
    strategy = Strategies.query.get(id)

    if not strategy:
        return jsonify({"msg": "Strategy not found"}), 404

    # Validasi input yang di-update
    if 'status' in data and data.get('status') not in ['active', 'non active']:
        return jsonify({"msg": "Status must be 'active' or 'non active'"}), 400
    
    strategy.nama = data.get('nama', strategy.nama)
    strategy.keterangan = data.get('keterangan', strategy.keterangan)
    strategy.status = data.get('status', strategy.status)

    db.session.commit()

    return jsonify({"msg": "Strategy updated successfully"}), 200

# Delete Strategy by ID (Menghapus Strategy Berdasarkan ID)
@strategies_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_strategy(id):
    strategy = Strategies.query.get(id)

    if not strategy:
        return jsonify({"msg": "Strategy not found"}), 404

    db.session.delete(strategy)
    db.session.commit()

    return jsonify({"msg": "Strategy deleted successfully"}), 200
