from .extensions import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=True)
    telp = db.Column(db.String(20), nullable=True)
    role = db.Column(db.Enum('admin', 'user'), nullable=False)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer = db.Column(db.String(255), nullable=False)
    treatment = db.Column(db.String(255), nullable=False)
    total = db.Column(db.String(255), nullable=False)

class Strategies(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), nullable=False)
    keterangan = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('active', 'non active'), nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    min_support = db.Column(db.Float, nullable=False)
    min_confidence = db.Column(db.Float, nullable=False)
    durasi = db.Column(db.Integer, nullable=True)
    tanggal_mulai = db.Column(db.Date, nullable=True)
    tanggal_selesai = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('active', 'non active'), nullable=False)

class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    antecedents = db.Column(db.String(255), nullable=False)
    consequents = db.Column(db.String(255), nullable=False)
    antecedent_support = db.Column(db.Float, nullable=False)
    consequent_support = db.Column(db.Float, nullable=False)
    support = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    lift = db.Column(db.Float, nullable=True, default=None)  # Memungkinkan NULL
    relationship = db.Column(db.String(50), nullable=True, default=None)  # Memungkinkan NULL