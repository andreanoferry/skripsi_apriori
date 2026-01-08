import os

class Config:
    # Secret Key (Boleh ganti sembarang)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-sangat-aman'

    # AMBIL DATA DARI RAILWAY (Variabel yang tadi kamu paste)
    DB_HOST = os.environ.get('MYSQLHOST')
    DB_USER = os.environ.get('MYSQLUSER')
    DB_PASSWORD = os.environ.get('MYSQLPASSWORD')
    DB_NAME = os.environ.get('MYSQLDATABASE')
    DB_PORT = os.environ.get('MYSQLPORT')

    # LOGIKA CERDAS:
    # Jika variabel MYSQLHOST ada (artinya sedang di Railway), pakai MySQL.
    # Jika tidak ada (artinya di laptop), pakai SQLite.
    if DB_HOST:
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Fallback ke SQLite jika running di laptop tanpa setting env
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False