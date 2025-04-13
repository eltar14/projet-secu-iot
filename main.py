import cv2
from ultralytics import YOLO
import time
from datetime import datetime
import json
import os
from db_utils import send_detection_to_api
from discord_utils import send_discord_embed_with_image
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

SAVE_DIR = os.environ.get('SAVE_DIR')
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK_URL')
API_URL = os.environ.get("API_URL")
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
VIDEO_CODEC = os.environ.get("VIDEO_CODEC", "avc1")


def encrypt_file(input_path, output_path, key):
    """
    Lit le contenu du fichier input_path, le chiffre et l'enregistre dans output_path.
    """
    try:
        with open(input_path, 'rb') as file_in:
            data = file_in.read()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        with open(output_path, 'wb') as file_out:
            file_out.write(encrypted_data)
        return True
    except Exception as e:
        print(f"Erreur lors du chiffrement : {e}")
        return False



def main(model_path, max_fps=4, no_detection_timeout=2):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam.")
        return()

    frame_delay = 1.0 / max_fps
    detected_ids = set()
    alert_active = False
    video_writer = None
    last_detection_time = None
    video_filename = None
    video_path = None
    detection_frame_count = 0

    fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)

    while True:
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire l'image.")
            break

        results = model.predict(frame, imgsz=192, classes=[0,], verbose=False)
        detection_dict = make_detection_dict(results[0].boxes, results[0].names)
        current_ids = set(detection_dict.keys())

        now = time.time()

        if current_ids:
            print(f"current IDs --- detecte IDs : {current_ids} --- {detected_ids}")
            last_detection_time = now

            # Si ce sont de nouvelles détections
            if not alert_active:
                alert_active = True
                detection_frame_count = 1
                ts = datetime.now()
                timestamp = ts.strftime('%Y-%m-%d_%H-%M-%S')
                video_filename = f"detection_{timestamp}.mp4"
                video_path = os.path.join(SAVE_DIR, video_filename)
                video_writer = cv2.VideoWriter(video_path, fourcc, max_fps, (frame.shape[1], frame.shape[0]))

                """# capture une image fixe pour l alerte + BDD
                image_name = f"detection_{timestamp}.jpg"
                image_path = os.path.join(SAVE_DIR, image_name)
                cv2.imwrite(image_path, frame)"""

                send_detection_to_api(
                    video_filename,
                    ts.strftime('%Y-%m-%d %H:%M:%S'),
                    detection_dict,
                    API_URL
                )

                """send_discord_embed_with_image(
                    DISCORD_WEBHOOK,
                    "ALERT",
                    f"Une intrusion a été détectée à {timestamp} : {json.dumps(detection_dict)}",
                    os.path.abspath(image_path)
                )"""
            else:
                detection_frame_count += 1

        if detection_frame_count == 3:
            # capture image + envoi API + Discord
            image_name = f"detection_{timestamp}.jpg"
            image_path = os.path.join(SAVE_DIR, image_name)
            cv2.imwrite(image_path, frame)

            send_detection_to_api(
                video_filename,
                ts.strftime('%Y-%m-%d %H:%M:%S'),
                detection_dict,
                API_URL
            )

            send_discord_embed_with_image(
                DISCORD_WEBHOOK,
                "ALERT",
                f"Une intrusion a été détectée à {timestamp} : {json.dumps(detection_dict)}",
                os.path.abspath(image_path)
            )


        if alert_active:
            video_writer.write(frame)

            # si plus aucune détection depuis x secondes
            if last_detection_time and (now - last_detection_time) > no_detection_timeout:
                print("Fin d'enregistrement.")
                alert_active = False
                detected_ids.clear()
                video_writer.release()
                video_writer = None
                last_detection_time = None

                if ENCRYPTION_KEY is None:
                    print("Cle de chiffrement non trouvée dans le fichier .env.")
                else:
                    encrypted_video_path = video_path + ".enc"
                    if encrypt_file(video_path, encrypted_video_path, ENCRYPTION_KEY):
                        # supprimer le fichier en clair si le chiffrement est reussi
                        os.remove(video_path)
                        print(f"Vidéo chiffrée et sauvegardée : {encrypted_video_path}")
                    else:
                        print("Echec du chiffrement de la vidéo.")


                video_filename = None
                video_path = None

        else:
            detected_ids.clear()

        result_frame = results[0].plot()
        cv2.imshow("YOLO Detection", result_frame)

        elapsed_time = time.time() - start_time
        time.sleep(max(0, frame_delay - elapsed_time))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()


def make_detection_dict(boxes, names):
    """
    returns a dictionnary as detected_object : how many of it detected
    :param boxes: object from results from model.predict
    :param names: object from results from model.predict
    :return:
    """
    occurence_list = [[x, boxes.cls.tolist().count(x)] for x in set(boxes.cls.tolist())]
    return {names[elt[0]]: elt[1] for elt in occurence_list}



if __name__ == "__main__":
    main(model_path='models/yolo11n_ncnn_model_192')
