import os

class Config:
    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv('SECRET_KEY', 'rahasia-skripsi-super-aman')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'rahasia-jwt-token-aman')
    JWT_ACCESS_TOKEN_EXPIRES = False

    # =========================
    # DATABASE (WAJIB MYSQL)
    # =========================
    DATABASE_URL = os.getenv('DATABASE_URL')

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL TIDAK TERDETEKSI! "
            "Pastikan DATABASE_URL sudah diset di Railway."
        )

    # Railway biasanya pakai mysql:// → SQLAlchemy perlu mysql+pymysql://
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "mysql://", "mysql+pymysql://", 1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
