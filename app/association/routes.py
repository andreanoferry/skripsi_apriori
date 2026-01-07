from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import and_
import os, json
from datetime import datetime

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules as ml_assoc_rules
from mlxtend.preprocessing import TransactionEncoder

from ..models import Association, Transactions
from ..extensions import db
from . import association_bp


# =========================
# Helpers
# =========================
def _results_path() -> str:
    base = current_app.instance_path
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "association_steps.json")


def association_rules_compat(fi_df: pd.DataFrame, metric: str = "confidence", min_threshold: float = 0.5) -> pd.DataFrame:
    """Compat untuk mlxtend versi berbeda."""
    try:
        return ml_assoc_rules(fi_df, metric=metric, min_threshold=min_threshold)
    except TypeError:
        return ml_assoc_rules(fi_df, metric=metric, min_threshold=min_threshold, num_itemsets=len(fi_df))


def normalize_rules_df(df_rules: pd.DataFrame):
    """Konversi rules: frozenset -> list."""
    out = []
    if df_rules is None or df_rules.empty:
        return out
    for _, r in df_rules.iterrows():
        ants = sorted(list(r["antecedents"])) if "antecedents" in r else []
        cons = sorted(list(r["consequents"])) if "consequents" in r else []
        out.append({
            "antecedents": ants,
            "consequents": cons,
            "antecedent_support": float(r.get("antecedent support", r.get("antecedent_support", 0.0))),
            "consequent_support": float(r.get("consequent support", r.get("consequent_support", 0.0))),
            "support": float(r.get("support", 0.0)),
            "confidence": float(r.get("confidence", 0.0)),
            "lift": float(r.get("lift", 0.0)),
            "relationship": "Strong" if float(r.get("lift", 0.0)) > 1.0 else "Weak",
        })
    return out


def serialize_fi_df(fi_df: pd.DataFrame):
    out = []
    if fi_df is None or fi_df.empty:
        return out
    for _, r in fi_df.iterrows():
        itemsets = sorted(list(r.get("itemsets", [])))
        out.append({
            "itemsets": itemsets,
            "support": float(r.get("support", 0.0))
        })
    return out


def safe_min_threshold(n_tx: int) -> float:
    if n_tx <= 0:
        return 1e-6
    return max(1.0 / float(n_tx), 1e-6)


def _write_steps_log(steps_log: dict):
    try:
        path = _results_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(steps_log, f, ensure_ascii=False, indent=2)
        print(
            f"[association] Steps log written to {path} "
            f"(RAW={len(steps_log.get('association_rules_raw', []))}, "
            f"FILTERED={len(steps_log.get('association_rules', []))}, "
            f"FI={len(steps_log.get('frequent_itemsets', []))}, "
            f"TX_RAW={len(steps_log.get('transactions_raw', []))})"
        )
    except Exception as e:
        print(f"[association] Error writing steps log: {e}")


def _read_steps_log() -> dict:
    path = _results_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"[association] Steps log loaded from {path}.")
            return data
        except Exception as e:
            print(f"[association] Error reading steps log: {e}")
    return {
        "transactions_raw": [],
        "transactions_list": [],
        "one_hot_encoded": {},
        "frequent_itemsets": [],
        "association_rules_raw": [],
        "association_rules": []
    }


def _transactions_to_ohe(transactions_list):
    te = TransactionEncoder()
    te_ary = te.fit(transactions_list).transform(transactions_list)
    df_trans = pd.DataFrame(te_ary, columns=te.columns_)
    return df_trans


# ======================================================
#  FIXED APRIORI 
# ======================================================
def _compute_steps(transactions, min_support=0.01, min_confidence=0.01):
    """
    Pipeline:
      1. OHE
      2. Frequent itemsets (pakai min_support user)
      3. association_rules_raw  = semua rules dari frequent itemsets (tanpa filter confidence)
      4. association_rules      = rules yang lolos min_confidence user
    """
    # Raw rows
    transactions_raw = []
    for t in transactions:
        try:
            tanggal_str = t.tanggal.strftime("%Y-%m-%d") if getattr(t, "tanggal", None) else None
        except Exception:
            tanggal_str = str(getattr(t, "tanggal", ""))
        transactions_raw.append({
            "id": getattr(t, "id", None),
            "tanggal": tanggal_str,
            "customer": getattr(t, "customer", None),
            "treatment": getattr(t, "treatment", None),
            "total": getattr(t, "total", None),
        })

    # List item
    df_treatment = pd.DataFrame([{"treatment": r["treatment"]} for r in transactions_raw], columns=["treatment"])
    transactions_list = df_treatment["treatment"].apply(
        lambda x: x.split(" + ") if isinstance(x, str) else []
    ).tolist()

    if len(transactions_list) == 0:
        return {
            "transactions_raw": [],
            "transactions_list": [],
            "one_hot_encoded": {},
            "frequent_itemsets": [],
            "association_rules_raw": [],
            "association_rules": []
        }

    df_trans = _transactions_to_ohe(transactions_list)

    # Guard
    n_tx = len(transactions_list)
    ms = min_support if (0 < float(min_support) <= 1) else 0.01
    mc = min_confidence if (0 < float(min_confidence) <= 1) else 0.01

    # Optional: hanya 1–3 itemset
    max_len = 3

    # ===== Frequent Itemsets =====
    fi = apriori(df_trans, min_support=ms, use_colnames=True, max_len=max_len)

    # ===== RAW RULES: semua rules dari frequent itemsets =====
    eps = safe_min_threshold(n_tx)   # tidak memfilter confidence
    rules_raw = association_rules_compat(fi, metric="confidence", min_threshold=eps)

    # ===== FILTERED RULES =====
    rules = association_rules_compat(fi, metric="confidence", min_threshold=mc)

    steps_log = {
        "transactions_raw": transactions_raw,
        "transactions_list": transactions_list,
        "one_hot_encoded": df_trans.to_dict(orient="list"),
        "frequent_itemsets": serialize_fi_df(fi.sort_values("support", ascending=False)),
        "association_rules_raw": normalize_rules_df(rules_raw),
        "association_rules": normalize_rules_df(rules)
    }

    return steps_log


# =========================
# Routes
# =========================
@association_bp.route("/", methods=["POST"])
@jwt_required()
def create_association():
    data = request.json
    start_date = data.get("tanggal_mulai")
    end_date = data.get("tanggal_selesai")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    if not start_date or not end_date:
        return jsonify({"msg": "Start and end dates are required"}), 400

    if not data.get("min_support") or not data.get("min_confidence"):
        return jsonify({"msg": "Incomplete data"}), 400

    try:
        min_support = float(data["min_support"])
        min_confidence = float(data["min_confidence"])
        if not (0 < min_support <= 1) or not (0 < min_confidence <= 1):
            return jsonify({"msg": "min_support and min_confidence must be in (0,1]."}), 400
    except ValueError:
        return jsonify({"msg": "min_support/min_confidence must be numbers"}), 400

    # Clear old
    db.session.query(Association).delete()
    db.session.commit()

    # Get transactions
    transactions = Transactions.query.filter(
        and_(Transactions.tanggal >= start_date, Transactions.tanggal <= end_date)
    ).all()

    if not transactions:
        return jsonify({"msg": f"No transactions found between {start_date} and {end_date}"}), 404

    # Compute main pipeline
    steps_log = _compute_steps(transactions, min_support=min_support, min_confidence=min_confidence)

    # Save FILTERED
    for r in steps_log.get("association_rules", []):
        db.session.add(Association(
            antecedents=json.dumps(r["antecedents"]),
            consequents=json.dumps(r["consequents"]),
            antecedent_support=r["antecedent_support"],
            consequent_support=r["consequent_support"],
            support=r["support"],
            confidence=r["confidence"],
            lift=r["lift"],
            relationship=r["relationship"]
        ))
    db.session.commit()

    _write_steps_log(steps_log)

    return jsonify({"msg": "Association added successfully"}), 201


@association_bp.route("/", methods=["GET"])
def get_all_association():
    try:
        associations = Association.query.all()
        final_associations = []
        for a in associations or []:
            try:
                final_associations.append({
                    "id": a.id,
                    "antecedents": json.loads(a.antecedents or "[]"),
                    "consequents": json.loads(a.consequents or "[]"),
                    "antecedent_support": a.antecedent_support,
                    "consequent_support": a.consequent_support,
                    "support": a.support,
                    "confidence": a.confidence,
                    "lift": a.lift,
                    "relationship": a.relationship,
                })
            except Exception as e:
                print(f"[association] Error processing association ID {a.id}: {e}")

        steps_log = _read_steps_log()

        need_fallback = (
            not steps_log.get("association_rules_raw") and
            not steps_log.get("frequent_itemsets") and
            not steps_log.get("transactions_list")
        )
        if need_fallback:
            print("[association] Fallback recompute.")
            all_tx = Transactions.query.order_by(Transactions.tanggal.asc()).all()
            steps_log = _compute_steps(all_tx, min_support=0.01, min_confidence=0.01)

        return jsonify({
            "steps_log": steps_log,
            "final_associations": final_associations
        }), 200

    except Exception as e:
        print(f"[association] Unexpected error: {e}")
        return jsonify({"msg": "Internal Server Error"}), 500


def run_apriori_logic(setting):
    start_date = setting.tanggal_mulai
    end_date = setting.tanggal_selesai
    try:
        min_support = float(setting.min_support)
        min_confidence = float(setting.min_confidence)
    except Exception:
        raise ValueError("min_support/min_confidence invalid")

    if not (0 < min_support <= 1) or not (0 < min_confidence <= 1):
        raise ValueError("min_support & min_confidence must be in (0,1].")

    db.session.query(Association).delete()
    db.session.commit()

    transactions = Transactions.query.filter(
        and_(Transactions.tanggal >= start_date, Transactions.tanggal <= end_date)
    ).all()

    if not transactions:
        return {"msg": f"No transactions found", "raw_count": 0, "filtered_count": 0}

    steps_log = _compute_steps(transactions, min_support=min_support, min_confidence=min_confidence)

    filtered_count = 0
    for r in steps_log.get("association_rules", []):
        db.session.add(Association(
            antecedents=json.dumps(r["antecedents"]),
            consequents=json.dumps(r["consequents"]),
            antecedent_support=r["antecedent_support"],
            consequent_support=r["consequent_support"],
            support=r["support"],
            confidence=r["confidence"],
            lift=r["lift"],
            relationship=r["relationship"]
        ))
        filtered_count += 1
    db.session.commit()

    _write_steps_log(steps_log)

    return {
        "msg": "Apriori executed via run_apriori_logic",
        "raw_count": len(steps_log["association_rules_raw"]),
        "filtered_count": filtered_count
    }
