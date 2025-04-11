from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)

from dashboard.auth import login_required, user_exist
from dashboard.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    if g.user:
        return redirect(url_for('dashboard.dashboard'))
    
    if user_exist():
        return render_template('auth/login.html')
    else:
        return render_template('auth/register.html')
    
@bp.route('/dashboard', methods=('GET', ))
@login_required
def dashboard():
    return render_template('dashboard.html')


@bp.route('/static/images/<path:filename>', methods=('GET', ))
@login_required
def serve_static(filename):
    return send_from_directory('static/images', filename)