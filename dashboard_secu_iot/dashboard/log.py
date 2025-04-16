from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from dashboard.auth import login_required, user_exist
from dashboard.db import get_db

bp = Blueprint('log', __name__, url_prefix="/log")

    
@bp.route('/', methods=('GET', ))
@login_required
def dashboard():
    try:
        with open("dashboard/logs/info.log", "r") as log_file:
            logs = log_file.readlines()
    except FileNotFoundError:
        logs = ["No logs found."]

    logs = logs[::-1]  # Reverse to show latest first
    return render_template('log.html', logs=logs)