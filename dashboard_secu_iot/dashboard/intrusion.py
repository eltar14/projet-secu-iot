from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from dashboard.auth import login_required, user_exist
from dashboard.db import get_db

bp = Blueprint('intrusion', __name__, url_prefix="/intrusion")

    
@bp.route('/', methods=('GET', ))
@login_required
def dashboard():
    return render_template('intrusion.html')