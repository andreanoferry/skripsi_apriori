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
    SECRET_KEY = os.getenv('SECRET_KEY', 'rahasia-skripsi-super-aman')

    # 2. DATABASE CONFIGURATION (BAGIAN KRUSIAL - UPDATE INI)
    # Kita ambil dari env var, bisa jadi namanya MYSQL_URL atau DATABASE_URL
    uri = os.getenv('MYSQL_URL') or os.getenv('DATABASE_URL') or 'sqlite:///skripsi.db'

    # PERBAIKAN PENTING:
    # Jika URL dimulai dengan 'mysql://', kita ubah jadi 'mysql+pymysql://'
    # agar Flask bisa menggunakan driver pymysql dengan benar di Railway.
    if uri and uri.startswith('mysql://'):
        uri = uri.replace('mysql://', 'mysql+pymysql://', 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3. JWT CONFIGURATION
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'rahasia-jwt-token-aman')
    JWT_ACCESS_TOKEN_EXPIRES = False