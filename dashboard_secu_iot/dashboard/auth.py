import functools

from flask import (
    Blueprint, g, redirect, request, session, url_for, jsonify, make_response, current_app
)
import os
import bcrypt
import jwt
from datetime import datetime

from dashboard.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('POST', ))
def login():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    
    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT * FROM credentials WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), user[2].encode('utf-8'))

    if password_hash == user[1].encode('utf-8'):
        session.clear()

        session["jwt_token"] = jwt.encode({"email": user[0]}, os.getenv("SECRET_KEY"), algorithm="HS256")

        current_app.logger.info(f"User {email} logged in successfully.")

        with open("dashboard/logs/info.log", "a") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - INFO - LOGIN\n")

        return jsonify({"redirect": url_for('dashboard.dashboard')}), 200
    
    return jsonify({"error": "Invalid email or password"}), 401


@bp.route('/register', methods=('POST', ))
def register():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    confirm_password = request.get_json()["confirm_password"]

    db = get_db()
    cur = db.cursor()

    issues = []

    if len(password) < 8:
        issues.append("Must be at least 8 characters long.")
    if len(password) > 64:
        issues.append("Must be at most 64 characters long.")
    if not any(char.isupper() for char in password):
        issues.append("Must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        issues.append("Must contain at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        issues.append("Must contain at least one number.")
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        issues.append("Must contain at least one special character.")
    if any(common in password.lower() for common in ["password", "123456", "qwerty"]):
        issues.append("Cannot contain common passwords.")

    if issues:
        return jsonify({"error": issues}), 400

    cur.execute('SELECT * FROM credentials WHERE email = %s', (email,))
    user = cur.fetchone()

    if user:
        return jsonify({"redirect": url_for('auth.login')}), 200

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    
    password_salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), password_salt)

    cur.execute(
        'INSERT INTO credentials (email, password_hash, password_salt) VALUES (%s, %s, %s)',
        (email, password_hash.decode('utf-8'), password_salt.decode('utf-8'))
    )

    cur.close()

    session.clear()
    session["jwt_token"] = jwt.encode({"email": email}, os.getenv("SECRET_KEY"), algorithm="HS256")
    return jsonify({"redirect": url_for('dashboard.dashboard')})


@bp.route('/logout', methods=('POST', ))
def logout():
    session.clear()
    with open("dashboard/logs/info.log", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - INFO - LOGOUT\n")

    return jsonify({"redirect": url_for("index")}), 200


@bp.before_app_request
def load_logged_in_user():
    if "jwt_token" not in session:
        g.user = None
        return
    user_email =  jwt.decode(session["jwt_token"], os.getenv("SECRET_KEY"), algorithms="HS256")["email"]

    if user_email is None:
        g.user = None
    else:
        cur = get_db().cursor()
        cur.execute(
            'SELECT * FROM credentials WHERE email = %s', (user_email, )
        )
        g.user = cur.fetchone()
        cur.close()


def user_exist():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM credentials')
    user = cur.fetchone()
    cur.close()
    return user is not None



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
