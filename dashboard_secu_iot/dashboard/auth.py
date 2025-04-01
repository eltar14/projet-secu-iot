import functools

from flask import (
    Blueprint, g, redirect, request, session, url_for, jsonify, make_response
)
import os
import bcrypt
import jwt

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

        return redirect(url_for('dashboard.dashboard'))
    
    return jsonify({"error": "Invalid email or password"}), 401


@bp.route('/register', methods=('POST', ))
def register():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    confirm_password = request.get_json()["confirm_password"]

    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT * FROM credentials WHERE email = %s', (email,))
    user = cur.fetchone()

    if user:
        return redirect(url_for('auth.login'))

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
    return redirect(url_for('dashboard.dashboard'))


@bp.route('/logout', methods=('POST', ))
def logout():
    print("logout")
    session.clear()
    return redirect(url_for('index'))


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

