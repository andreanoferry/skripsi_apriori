from flask import Blueprint

strategies_bp = Blueprint('strategies', __name__)
from . import routes
