from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import Transactions
from ..extensions import db
from . import transactions_bp

# =========================
# Helpers
# =========================
def _extract_id_user():
    """
    Ambil id_user dari JWT secara robust:
    - identity bisa int / str / dict
    - kalau tidak ada di identity, coba dari additional claims
    - kalau identity adalah string JSON (warisan lama), coba json.loads
    """
    identity = get_jwt_identity()
    claims = get_jwt()

    # identity langsung integer
    if isinstance(identity, int):
        return identity

    # identity string -> bisa "123" atau JSON string lama
    if isinstance(identity, str):
        # 1) coba parse sebagai int langsung
        try:
            return int(identity)
        except ValueError:
            pass
        # 2) coba parse sebagai JSON lama
        try:
            import json
            d = json.loads(identity)
            for k in ("user_id", "id", "uid"):
                if k in d:
                    try:
                        return int(d[k])
                    except (TypeError, ValueError):
                        continue
        except Exception:
            pass

    # identity dict (format baru dari login yang sudah diperbaiki)
    if isinstance(identity, dict):
        for k in ("user_id", "id", "uid"):
            v = identity.get(k)
            try:
                return int(v)
            except (TypeError, ValueError):
                continue

    # fallback dari additional claims
    for k in ("user_id", "id", "uid"):
        v = claims.get(k)
        try:
            return int(v)
        except (TypeError, ValueError):
            continue

    return None


def _to_number(val, field_name="total"):
    """Validasi numerik; kembalikan float untuk validasi, tapi simpan sebagai string (sesuai model)."""
    try:
        return float(val)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number")


# =========================
# Create Transaction (Menambahkan Transaksi)
# =========================
@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    data = request.get_json(silent=True) or {}

    customer = (data.get('customer') or '').strip()
    treatment = (data.get('treatment') or '').strip()
    # Hindari 'if not data.get("total")' karena 0 dianggap falsy
    if customer == '' or treatment == '' or ('total' not in data or data.get('total') is None):
        return jsonify({"msg": "Incomplete data"}), 400

    # Validasi numerik, tapi simpan sebagai string (model kolom String)
    try:
        _ = _to_number(data.get('total'), "total")
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

    id_user = _extract_id_user()
    if id_user is None:
        return jsonify({"msg": "user_id missing in JWT"}), 401

    new_transaction = Transactions(
        id_user=id_user,
        customer=customer,
        treatment=treatment,
        total=str(data.get('total'))  # ← model expects String(255)
        # tanggal: pakai default model (utcnow); jika ingin custom, parse data.get('tanggal')
    )
    try:
        db.session.add(new_transaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to create transaction", "error": str(e)}), 500

    return jsonify({"msg": "Transaction created successfully", "transaction": {
        "id": new_transaction.id,
        "id_user": new_transaction.id_user,
        "customer": new_transaction.customer,
        "treatment": new_transaction.treatment,
        "total": new_transaction.total,
        "tanggal": str(new_transaction.tanggal)
    }}), 201


# =========================
# Read All Transactions (Mendapatkan Semua Transaksi)
# =========================
@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_transactions():
    transactions = Transactions.query.all()
    if not transactions:
        return jsonify([]), 200  # kosong tapi OK

    result = []
    for t in transactions:
        result.append({
            "id": t.id,
            "id_user": t.id_user,
            "customer": t.customer,
            "treatment": t.treatment,
            "total": t.total,
            "tanggal": str(t.tanggal)
        })
    return jsonify(result), 200


# =========================
# Read Single Transaction by ID
# =========================
@transactions_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_transaction(id):
    t = Transactions.query.get(id)
    if not t:
        return jsonify({"msg": "Transaction not found"}), 404

    return jsonify({
        "id": t.id,
        "id_user": t.id_user,
        "customer": t.customer,
        "treatment": t.treatment,
        "total": t.total,
        "tanggal": str(t.tanggal)
    }), 200


# =========================
# Update Transaction
# =========================
@transactions_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_transaction(id):
    data = request.get_json(silent=True) or {}
    t = Transactions.query.get(id)
    if not t:
        return jsonify({"msg": "Transaction not found"}), 404

    id_user = _extract_id_user()
    if id_user is None:
        return jsonify({"msg": "user_id missing in JWT"}), 401

    # total (jika ada) harus numerik, tapi simpan sebagai string
    if 'total' in data and data.get('total') is not None:
        try:
            _ = _to_number(data.get('total'), "total")
            t.total = str(data.get('total'))
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400

    if 'customer' in data:
        val = (data.get('customer') or '').strip()
        if val:
            t.customer = val
    if 'treatment' in data:
        val = (data.get('treatment') or '').strip()
        if val:
            t.treatment = val

    t.id_user = id_user

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to update transaction", "error": str(e)}), 500

    return jsonify({"msg": "Transaction updated successfully"}), 200


# =========================
# Delete Transaction
# =========================
@transactions_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    t = Transactions.query.get(id)
    if not t:
        return jsonify({"msg": "Transaction not found"}), 404

    try:
        db.session.delete(t)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to delete transaction", "error": str(e)}), 500

    return jsonify({"msg": "Transaction deleted successfully"}), 200
