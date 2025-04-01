import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

API_URL = os.environ.get("API_URL")


def send_detection_to_api(video_path, timestamp, detection_dict):
    try:
        data = {
            'video_path': video_path,
            'timestamp': timestamp,
            'detection': json.dumps(detection_dict),
            'duration': 1
        }

        response = requests.post(API_URL, data=data, timeout=10)
        response.raise_for_status()
        print("Detection envoyee au serveur.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la detection : {e}")
