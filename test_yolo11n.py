import cv2
from ultralytics import YOLO
import time
from datetime import datetime
import json
import os
from db_utils import insert_detection

SAVE_DIR = "/home/user/projet-secu-iot/SAVE_DIR"


def main(model_path, max_fps=4):
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam.")
        return()

    frame_delay = 1.0 / max_fps
    detected_ids = set()

    while True:
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire l'image.")
            break
        #frame = cv2.resize(frame, (426, 240))
        results = model.predict(frame, imgsz=96, classes=[0,], verbose=False)
        #annotated_frame = results.render()[0]
        detection_dict = make_detection_dict(results[0].boxes, results[0].names)

        current_ids = set([tuple(sorted(detection_dict.items()))])

        if current_ids and not current_ids.issubset(detected_ids):
            detected_ids.update(current_ids)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            image_name = f"detection_{timestamp.replace(':', '-')}.jpg"
            image_path = os.path.join(SAVE_DIR, image_name)

            cv2.imwrite(image_path, frame)

            insert_detection(
                os.path.abspath(image_path),
                timestamp,
                json.dumps(detection_dict)
            )

            print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} --- {detection_dict}")

        result_frame = results[0].plot()
        cv2.imshow("YOLO Detection", result_frame)

        elapsed_time = time.time() - start_time
        sleep_time = max(0, frame_delay - elapsed_time)
        time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def make_detection_dict(boxes, names):
    occurence_list = [[x, boxes.cls.tolist().count(x)] for x in set(boxes.cls.tolist())]
    mon_dict = {}
    for elt in occurence_list:
        mon_dict[names[elt[0]]] = elt[1]
    return mon_dict

def dict_to_json(detection_dict):
    return json.dumps(detection_dict)

if __name__ == "__main__":
    main(model_path='models/yolo11n_ncnn_model_96')