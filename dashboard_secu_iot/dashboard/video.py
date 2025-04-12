from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)

import psycopg2.extras

from dashboard.auth import login_required

from dashboard.db import get_db

bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route('/add', methods=('POST', ))
def add_video():
    if request.remote_addr != '127.0.0.1':
        return "Access denied", 403

    video_path = request.form['video_path']
    timestamp = request.form['timestamp']
    duration = request.form['duration']
    detection = request.form['detection']

    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO video (file_path, timestamp, duration, description) VALUES (%s, %s, %s, %s)',
        ('/static/images' + video_path, 'CURRENT_TIMESTAMP', duration, detection)
    )

    return "Video added successfully", 200


@bp.route('/get' , methods=('GET', ))
@login_required
def get_video():
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM video WHERE intrusion IS NULL ORDER BY timestamp DESC')
    videos = cur.fetchall()
    cur.close()

    print(url_for('static', filename='video/aaa.mp4'))

    return [{k:v for k, v in record.items()} for record in videos], 200


@bp.route('/get_intrusion' , methods=('GET', ))
@login_required
def get_intrusion_video():
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM video WHERE intrusion IS True ORDER BY timestamp DESC')
    videos = cur.fetchall()
    cur.close()

    print(url_for('static', filename='video/aaa.mp4'))

    return [{k:v for k, v in record.items()} for record in videos], 200


@bp.route('/set_intrusion' , methods=('POST', ))
@login_required
def set_intrusion_video():
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    intrusion = request.get_json()['intrusion']
    video_id = request.get_json()['video_id']

    cur.execute('SELECT * FROM video WHERE id = %s', (video_id, ))
    video = cur.fetchone()

    print(video['intrusion'])

    if video is None:
        return "Video not found", 404
    if video['intrusion'] is not None:
        return "Video already set", 400


    cur.execute('UPDATE video SET intrusion = %s WHERE id = %s', (intrusion, video_id, ))
    db.commit()
    cur.close()

    return "Intrusion video updated successfully", 200