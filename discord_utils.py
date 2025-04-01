import requests
from typing import Optional


def send_discord_message(webhook_url: str, content: str) -> bool:
    """
    Envoie un message texte simple à un webhook Discord.
    """
    try:
        payload = {"content": content}
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            print(f"[Erreur] Message non envoyé: {response.status_code} - {response.text}")
            return False
        return True
    except Exception as e:
        print(f"[Exception] Erreur lors de l'envoi du message: {e}")
        return False


def send_discord_embed(webhook_url: str, title: str, description: str, color: int = 0x3498db) -> bool:
    """
    Envoie un embed Discord (titre, description, couleur).
    """
    try:
        embed = {
            "title": title,
            "description": description,
            "color": color
        }
        payload = {"embeds": [embed]}
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            print(f"[Erreur] Embed non envoyé: {response.status_code} - {response.text}")
            return False
        return True
    except Exception as e:
        print(f"[Exception] Erreur lors de l'envoi de l'embed: {e}")
        return False


def send_discord_image(webhook_url: str, content: str = "", image_path: Optional[str] = None) -> bool:
    """
    Envoie un message avec une image jointe (uploadée depuis le disque).
    """
    if not image_path:
        print("[Erreur] Aucun chemin d'image fourni.")
        return False

    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {"content": content}
            response = requests.post(webhook_url, data=data, files=files)
            if response.status_code != 204:
                print(f"[Erreur] Image non envoyée: {response.status_code} - {response.text}")
                return False
            return True
    except Exception as e:
        print(f"[Exception] Erreur lors de l'envoi de l'image: {e}")
        return False


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

