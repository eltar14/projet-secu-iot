from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)

from dashboard.db import get_db

bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route('/add', methods=('POST', ))
def add_video():
    if request.remote_addr != '127.0.0.1':
        return "Access denied", 403

    video_path = request.form['video_path']
    timestamp = request.form['timestamp']
    duration = request.form['duration']
    video_description = request.form['video_description']

    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO video (video_path, timestamp, duration, video_description) VALUES (%s, %s, %s, %s)',
        (video_path, timestamp, duration, video_description)
    )
