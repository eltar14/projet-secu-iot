import requests
from typing import Optional
import json

def send_discord_embed_with_image(webhook_url: str, title: str, description: str, image_path: str, color: int = 0x3498db) -> bool:
    """
    Envoie un embed Discord avec une image intégrée (affichée dans l'embed).
    """
    try:
        filename = image_path.split("/")[-1]
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "image": {
                "url": f"attachment://{filename}"
            }
        }

        with open(image_path, "rb") as f:
            files = {
                "file": (filename, f),
                "payload_json": (None, json.dumps({"embeds": [embed]}), "application/json")
            }
            response = requests.post(webhook_url, files=files)
            if response.status_code != 204:
                print(f"[Erreur] Embed avec image non envoyé: {response.status_code} - {response.text}")
                return False
            return True

    except Exception as e:
        print(f"[Exception] Erreur lors de l'envoi de l'embed avec image: {e}")
        return False

