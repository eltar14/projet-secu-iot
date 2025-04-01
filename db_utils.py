import requests
import os
import json

API_URL = os.environ.get("API_URL")
def send_detection_to_api(video_path, timestamp, detection_dict):
    try:
        with open(video_path, 'rb') as f:
            files = {'video': f}
            data = {
                'timestamp': timestamp,
                'detection': json.dumps(detection_dict)
            }
            response = requests.post(API_URL, data=data, files=files, timeout=10)
            response.raise_for_status()
            print("Detection envoyee au serveur.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la detection : {e}")
