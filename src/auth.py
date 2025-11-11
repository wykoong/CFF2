from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, current_app

OPERATOR_SESSION_KEY = "operator_id"

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(hash_, password: str) -> bool:
    return check_password_hash(hash_, password)

def login_operator(operator_id: int):
    session[OPERATOR_SESSION_KEY] = operator_id

def logout_operator():
    session.pop(OPERATOR_SESSION_KEY, None)

def get_current_operator_id():
    return session.get(OPERATOR_SESSION_KEY)