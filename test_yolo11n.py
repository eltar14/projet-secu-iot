import cv2
from ultralytics import YOLO
import time

def main(model_path, max_fps=4):
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam.")
        return()

    frame_delay = 1.0 / max_fps

    while True:
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire l'image.")
            break
        #frame = cv2.resize(frame, (426, 240))
        results = model.predict(frame, imgsz=96, classes=[0,])
        #annotated_frame = results.render()[0]
        result_frame = results[0].plot()
        cv2.imshow("YOLO Detection", result_frame)

        elapsed_time = time.time() - start_time
        sleep_time = max(0, frame_delay - elapsed_time)
        time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(model_path='models/yolo11n_ncnn_model_96')