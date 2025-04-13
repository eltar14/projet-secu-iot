from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, abort, Response, current_app
)

from cryptography.fernet import Fernet

from dashboard.auth import login_required, user_exist
from dashboard.db import get_db
import os

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



def decrypt_stream(path):
    fernet = Fernet(current_app.config['FRENET_KEY'])
    def generate():
        with open(path, 'rb') as f:
            encrypted_data = f.read()
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
            except Exception:
                abort(500, description="Decryption failed.")
            
            chunk_size = 1024 * 1024
            for i in range(0, len(decrypted_data), chunk_size):
                yield decrypted_data[i:i + chunk_size]

    return generate


@bp.route('/static/images/<path:filename>')
@login_required
def serve_decrypted_video(filename):
    encrypted_path = os.path.join(os.getcwd(), 'dashboard', 'static', 'images', filename + '.enc')

    if not os.path.exists(encrypted_path):
        abort(404)

    return Response(
        decrypt_stream(encrypted_path),
        mimetype='video/mp4',
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Accept-Ranges": "bytes"
        }
    )
