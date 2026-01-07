from flask_jwt_extended import get_jwt
from ..extensions import blacklist

def add_token_to_blacklist():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
