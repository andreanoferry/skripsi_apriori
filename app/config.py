import os
"""
from dotenv import load_dotenv
    
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = False  # 30 menit
    # CORS_ORIGINS = ["http://localhost:5000"]
"""


class Config:
    # 1. SECRET KEY
    # Mengambil dari Render, jika tidak ada pakai default 'rahasia-skripsi'
    SECRET_KEY = os.getenv('SECRET_KEY', 'rahasia-skripsi-super-aman')

    # 2. DATABASE CONFIGURATION (BAGIAN KRUSIAL)
    # Logika: Cek variabel 'SQLALCHEMY_DATABASE_URI' dulu.
    # Jika kosong, cek 'DATABASE_URL'.
    # Jika masih kosong, PAKSA pakai 'sqlite:///skripsi.db' (Fail-safe).
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or \
                              os.getenv('DATABASE_URL') or \
                              'sqlite:///skripsi.db'

    # Matikan notifikasi track modifications (biar hemat memori)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3. JWT CONFIGURATION
    # Sama, ambil dari Render, jika kosong pakai default
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'rahasia-jwt-token-aman')
    
    # Token tidak akan expired (sesuai settingan kamu sebelumnya)
    JWT_ACCESS_TOKEN_EXPIRES = False 

    # (Opsional) Jika nanti butuh settingan CORS
    # CORS_ORIGINS = ["*"]
