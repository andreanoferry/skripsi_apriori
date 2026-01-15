from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import select, and_, or_
import os, json
from datetime import datetime

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules as ml_assoc_rules
from mlxtend.preprocessing import TransactionEncoder

from ..models import Association, Transactions
from itertools import combinations
from ..extensions import db
from . import association_bp


# =========================
# Helpers
# =========================
def _results_path() -> str:
    # [KEMBALI KE ORIGINAL] Menggunakan folder instance bawaan Flask
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
        
        # [PERBAIKAN] Force delete file lama agar tidak ada data "hantu"
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

        with open(path, "w", encoding="utf-8") as f:
            # Gunakan default=str agar aman dari error tipe data
            json.dump(steps_log, f, ensure_ascii=False, indent=2, default=str)
            
        print(
            f"[association] Steps log written to {path} "
            f"(RAW={len(steps_log.get('association_rules_raw', []))}, "
            f"FILTERED={len(steps_log.get('association_rules', []))}, "
            f"FI={len(steps_log.get('frequent_itemsets', []))}, "
            f"CANDIDATES={len(steps_log.get('candidate_generation', []))}, "
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
        "candidate_generation": [],
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
#  FIXED APRIORI — SESUAI TEORI
# ======================================================
def _compute_steps(transactions, min_support=0.01, min_confidence=0.01):
    # [DEBUG 4] Parameter Mentah yang diterima fungsi
    print("\n" + "="*50)
    print(f"[DEBUG 4] _compute_steps dipanggil.")
    print(f"   -> transactions count: {len(transactions)}")
    print(f"   -> min_support (arg): {min_support} (Tipe: {type(min_support)})")
    print(f"   -> min_confidence (arg): {min_confidence} (Tipe: {type(min_confidence)})")
    print("="*50 + "\n")

    # 1. Preprocessing Transaksi
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

    df_treatment = pd.DataFrame([{"treatment": r["treatment"]} for r in transactions_raw], columns=["treatment"])
    transactions_list = df_treatment["treatment"].apply(
        lambda x: x.split(" + ") if isinstance(x, str) else []
    ).tolist()

    if len(transactions_list) == 0:
        print("[DEBUG] Transaksi kosong, return early.")
        return { "association_rules": [], "association_rules_raw": [], "frequent_itemsets": [] }

    # OHE
    df_trans = _transactions_to_ohe(transactions_list)

    # 2. Validasi Parameter (Guard)
    try:
        ms = float(min_support)
        if not (0 < ms <= 1): ms = 0.01
        
        mc = float(min_confidence)
        if not (0 < mc <= 1): mc = 0.01
    except:
        ms = 0.01
        mc = 0.01

    # [DEBUG 5] Setelah Validasi float & Logic
    print(f"[DEBUG 5] Nilai yang AKAN dipakai Apriori:")
    print(f"   -> ms (final): {ms}")
    print(f"   -> mc (final): {mc}")

    # ==========================================================
    # [LOGIC BARU] HITUNG CANDIDATE GENERATION (C1, C2, C3) MANUAL
    # ==========================================================
    print(f"[DEBUG 5.5] Menghitung Candidate Generation (C1, C2, C3)...")
    
    # Ambil semua item unik dari transaksi list
    unique_items = sorted(list(set([item for sublist in transactions_list for item in sublist])))
    total_trans = len(transactions_list)
    candidate_data = []

    # --- Generate C1, C2, C3 ---
    for k in range(1, 4): 
        for item_tuple in combinations(unique_items, k):
            # Hitung frekuensi kemunculan kombinasi
            count = sum(1 for t in transactions_list if set(item_tuple).issubset(set(t)))
            
            # Hitung support
            support = round(count / total_trans, 4) if total_trans > 0 else 0
            
            # Simpan data
            candidate_data.append({
                "items": ", ".join(item_tuple),
                "count": count,
                "support": support
            })
    
    # Urutkan berdasarkan support tertinggi
    candidate_data.sort(key=lambda x: x['support'], reverse=True)
    print(f"   -> Selesai. Total kandidat generated: {len(candidate_data)}")
    # ==========================================================

    # 3. Hitung Frequent Itemsets (Apriori)
    print(f"[DEBUG 6] Menjalankan mlxtend.apriori dengan min_support={ms}...")
    
    fi = apriori(df_trans, min_support=ms, use_colnames=True, max_len=3)

    # [DEBUG 7] HASIL APRIORI
    print("\n" + "*"*30)
    print(f"[DEBUG 7] HASIL APRIORI:")
    if not fi.empty:
        min_found = fi["support"].min()
        max_found = fi["support"].max()
        print(f"   -> Jumlah Itemset Ditemukan: {len(fi)}")
        print(f"   -> Support Terkecil di tabel: {min_found}")
        print(f"   -> Support Terbesar di tabel: {max_found}")
        
        if min_found < ms:
            print(f"   !!! BAHAYA: Ditemukan support {min_found} padahal request {ms} !!!")
        else:
            print(f"   -> OK: Semua support >= {ms}")
            
        print("   -> 5 Data Teratas:")
        print(fi.head(5))
    else:
        print("   -> HASIL KOSONG (0 Itemsets ditemukan)")
    print("*"*30 + "\n")

    # 4. Generate Rules [PERBAIKAN: CEK KOSONG]
    # Inisialisasi DataFrame kosong agar tidak error
    rules_raw = pd.DataFrame()
    rules = pd.DataFrame()

    # Hanya jalankan jika frequent itemset (fi) TIDAK kosong
    if not fi.empty:
        try:
            n_tx = len(transactions_list)
            eps = safe_min_threshold(n_tx)
            rules_raw = association_rules_compat(fi, metric="confidence", min_threshold=eps)
            rules = association_rules_compat(fi, metric="confidence", min_threshold=mc)
        except Exception as e:
            print(f"[ERROR] Gagal generate rules: {e}")

    steps_log = {
        "parameters": {                 # keterangan min support dan confidence
            "min_support": ms, 
            "min_confidence": mc 
        },
        "transactions_raw": transactions_raw,
        "transactions_list": transactions_list,
        "one_hot_encoded": df_trans.to_dict(orient="list"),
        "candidate_generation": candidate_data,
        "frequent_itemsets": serialize_fi_df(fi.sort_values("support", ascending=False)) if not fi.empty else [],
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
    # [DEBUG 1] Data Mentah Request
    data = request.get_json(silent=True) or {}
    print("\n" + "#"*50)
    print(f"[DEBUG 1] Request Masuk ke /process")
    print(f"   -> Data Mentah JSON: {data}")

    try:
        # Konversi Input
        min_support = float(data.get("min_support", 0.1))
        min_confidence = float(data.get("min_confidence", 0.5))
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # [DEBUG 2] Setelah Konversi Float
        print(f"[DEBUG 2] Parsing Input:")
        print(f"   -> min_support (float): {min_support}")
        print(f"   -> min_confidence (float): {min_confidence}")
        
    except ValueError:
        return jsonify({"msg": "Invalid support/confidence values"}), 400

    # Ambil Transaksi
    query = select(Transactions)
    if start_date and end_date:
        query = query.where(and_(Transactions.tanggal >= start_date, Transactions.tanggal <= end_date))
    
    transactions = db.session.execute(query).scalars().all()

    if not transactions:
        return jsonify({"msg": "No transactions found"}), 404

    # [DEBUG 3] Sebelum Masuk Fungsi Logic
    print(f"[DEBUG 3] Memanggil _compute_steps...")
    print(f"   -> Mengirim min_support: {min_support}")
    
    # --- PANGGIL FUNGSI LOGIC ---
    steps_log = _compute_steps(transactions, min_support=min_support, min_confidence=min_confidence)
    # ----------------------------

    # [PERBAIKAN LOKASI SIMPAN]
    # Simpan log ke file DULUAN sebelum berurusan dengan Database.
    # Ini memastikan file steps.json terupdate (kosong) meskipun nanti DB error.
    _write_steps_log(steps_log)

    # Hapus data lama & Simpan baru
    db.session.query(Association).delete()
    
    saved_count = 0
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
        saved_count += 1
    
    # Jika baris ini error, file JSON sudah aman tersimpan di atas
    db.session.commit()

    # [DEBUG 8] Ringkasan Akhir
    print(f"[DEBUG 8] Selesai.")
    print(f"   -> Rules disimpan ke DB: {saved_count}")
    print("#"*50 + "\n")

    return jsonify({
        "msg": "Association analysis completed",
        "steps": steps_log
    }), 201

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

        # [PERBAIKAN] Matikan Fallback (Auto-recompute)
        # Agar jika hasil kosong (0.9), tetap tampil kosong, tidak dipaksa balik ke 0.01
        # need_fallback = (...) 
        # if need_fallback: ...

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

    # Simpan file log
    _write_steps_log(steps_log)

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

    return {
        "msg": "Apriori executed via run_apriori_logic",
        "raw_count": len(steps_log["association_rules_raw"]),
        "filtered_count": filtered_count
    }