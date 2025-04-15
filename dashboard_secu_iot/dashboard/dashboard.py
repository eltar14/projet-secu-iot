from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, abort, Response, current_app
)

import re
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


@bp.route('/static/images/<path:filename>')
@login_required
def serve_decrypted_video(filename):
    encrypted_path = os.path.join(os.getcwd(), 'dashboard', 'static', 'images', filename + '.enc')
    if not os.path.exists(encrypted_path):
        abort(404)

    fernet = Fernet(current_app.config['FRENET_KEY'])
    with open(encrypted_path, 'rb') as f:
        try:
            decrypted_data = fernet.decrypt(f.read())
        except Exception:
            abort(500, description="Decryption failed.")

    range_header = request.headers.get('Range', None)
    if range_header:
        match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else len(decrypted_data) - 1
        else:
            start = 0
            end = len(decrypted_data) - 1
        length = end - start + 1

        response = Response(
            decrypted_data[start:end + 1],
            206,
            mimetype='video/mp4',
            direct_passthrough=True,
        )
        response.headers.add('Content-Range', f'bytes {start}-{end}/{len(decrypted_data)}')
        response.headers.add('Accept-Ranges', 'bytes')
        response.headers.add('Content-Length', str(length))
        return response

    return Response(
        decrypted_data,
        mimetype='video/mp4',
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(len(decrypted_data))
        }
    )