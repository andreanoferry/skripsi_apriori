from flask import request, jsonify, current_app, abort
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from sqlalchemy import select, update
from ..models import Settings
from ..extensions import db
from . import settings_bp
from ..association.routes import run_apriori_logic


# ---------- Utils ----------
def to_dict(setting: Settings):
    return {
        "id": setting.id,
        "min_support": setting.min_support,
        "min_confidence": setting.min_confidence,
        "durasi": setting.durasi,
        "tanggal_mulai": setting.tanggal_mulai.isoformat() if getattr(setting, "tanggal_mulai", None) else None,
        "tanggal_selesai": setting.tanggal_selesai.isoformat() if getattr(setting, "tanggal_selesai", None) else None,
        "status": setting.status,
    }


# ---------- Monitor Thread ----------
def monitor_duration(app, setting_id: int):
    """
    Loop selagi setting 'active':
    - tidur selama 'durasi' menit
    - jalankan run_apriori_logic(setting)
    - ulangi selama status masih 'active'
    Berhenti jika setting dihapus atau status != 'active'
    """
    with app.app_context():
        while True:
            setting = db.session.get(Settings, setting_id)

            # stop kalau setting hilang atau tidak active
            if not setting or setting.status != "active":
                print(f"[monitor] Stopping monitoring for Setting ID {setting_id}.")
                break

            duration_minutes = setting.durasi or 0
            remaining_time = max(0, int(duration_minutes) * 60)
            print(f"[monitor] Setting ID {setting_id}: sleeping {remaining_time} second(s).")

            sleep(remaining_time)

            # recheck setelah sleep
            setting = db.session.get(Settings, setting_id)
            if not setting or setting.status != "active":
                print(f"[monitor] Setting ID {setting_id} became non-active/removed after sleep. Stop.")
                break

            print(f"[monitor] Duration expired for Setting ID {setting_id}. Running Apriori.")
            try:
                run_apriori_logic(setting)
                print(f"[monitor] Apriori updated for Setting ID {setting_id}. Repeat loop.")
            except Exception as e:
                # log lalu lanjut loop
                print(f"[monitor] Error running Apriori for Setting ID {setting_id}: {e}")


def start_monitor_thread(setting_id: int):
    t = Thread(
        target=monitor_duration,
        args=(current_app._get_current_object(), setting_id),
        daemon=True,  # penting: jangan blokir shutdown
    )
    t.start()


# ---------- Helpers ----------
def deactivate_other_active_settings(exclude_id: int | None = None):
    """
    Nonaktifkan semua setting 'active' kecuali exclude_id (jika ada) secara bulk.
    """
    stmt = update(Settings).where(Settings.status == "active")
    if exclude_id is not None:
        stmt = stmt.where(Settings.id != exclude_id)
    stmt = stmt.values(status="non active")
    res = db.session.execute(stmt)
    db.session.commit()
    if res.rowcount:
        print(f"[deactivate] Deactivated {res.rowcount} active setting(s) (exclude_id={exclude_id}).")


# ---------- Routes ----------
@settings_bp.route("/", methods=["POST"])
@jwt_required()
def create_setting():
    data = request.get_json(silent=True) or {}

    # validasi sederhana
    required = ("min_support", "min_confidence", "status")
    if any(data.get(k) in (None, "") for k in required):
        return jsonify({"msg": "Incomplete data"}), 400

    if data.get("status") not in ["active", "non active"]:
        return jsonify({"msg": "Status must be 'active' or 'non active'"}), 400

    # jika aktif, nonaktifkan yang lain
    if data["status"] == "active":
        deactivate_other_active_settings()

    new_setting = Settings(
        min_support=data.get("min_support"),
        min_confidence=data.get("min_confidence"),
        durasi=data.get("durasi"),
        tanggal_mulai=data.get("tanggal_mulai"),
        tanggal_selesai=data.get("tanggal_selesai"),
        status=data.get("status"),
    )
    db.session.add(new_setting)
    db.session.commit()

    if new_setting.status == "active":
        start_monitor_thread(new_setting.id)

    return jsonify({"msg": "Setting created successfully", "data": to_dict(new_setting)}), 201


@settings_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_settings():
    rows = db.session.execute(select(Settings).order_by(Settings.id.desc())).scalars().all()
    if not rows:
        return jsonify({"msg": "No settings found"}), 404
    return jsonify([to_dict(r) for r in rows]), 200


@settings_bp.route("/active", methods=["GET"])
@jwt_required()
def get_active_setting():
    row = db.session.execute(
        select(Settings).where(Settings.status == "active").limit(1)
    ).scalars().first()

    if not row:
        return jsonify({"msg": "Active setting not found"}), 404

    return jsonify(to_dict(row)), 200


@settings_bp.route("/status/<int:id>", methods=["PUT"])
@jwt_required()
def update_setting_status(id: int):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")

    if new_status not in ["active", "non active"]:
        return jsonify({"msg": "Invalid status. Status must be 'active' or 'non active'"}), 400

    setting = db.session.get(Settings, id)
    if not setting:
        return jsonify({"msg": "Setting not found"}), 404

    if new_status == "active":
        deactivate_other_active_settings(exclude_id=id)
        # ubah status dulu supaya monitor langsung loop
        setting.status = "active"
        db.session.commit()
        start_monitor_thread(id)
    else:
        setting.status = "non active"
        db.session.commit()

    return jsonify({"msg": f"Setting {id} updated to {new_status} successfully", "data": to_dict(setting)}), 200


@settings_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_setting(id: int):
    data = request.get_json(silent=True) or {}
    setting = db.session.get(Settings, id)
    if not setting:
        return jsonify({"msg": "Setting not found"}), 404

    if "status" in data and data["status"] not in ["active", "non active"]:
        return jsonify({"msg": "Status must be 'active' or 'non active'"}), 400

    was_active = (setting.status == "active")

    # update kolom
    for field in ["min_support", "min_confidence", "durasi", "tanggal_mulai", "tanggal_selesai", "status"]:
        if field in data:
            setattr(setting, field, data[field])

    db.session.commit()

    # jika dari non-active → active
    if setting.status == "active" and not was_active:
        deactivate_other_active_settings(exclude_id=id)
        start_monitor_thread(id)

    return jsonify({"msg": "Setting updated successfully", "data": to_dict(setting)}), 200


@settings_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_setting(id: int):
    setting = db.session.get(Settings, id)  # <- 2.0 style
    if not setting:
        return jsonify({"msg": "Setting not found"}), 404

    db.session.delete(setting)
    db.session.commit()
    # thread akan berhenti sendiri karena setting sudah tidak ada saat dicek
    return jsonify({"msg": "Setting deleted successfully"}), 200
