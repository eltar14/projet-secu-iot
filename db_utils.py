import psycopg2
from db import DB_CONFIG

def insert_detection(image_path, timestamp, detection_json, id_detecteur=1):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO detection (timestamp_detection, info_detection, path_image_detection, real_detection, seen, id_detecteur)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (timestamp, detection_json, image_path, True, False, id_detecteur))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'insertion en base : {e}")
