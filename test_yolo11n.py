import cv2
from ultralytics import YOLO

def main(model_path, max_fps=10):
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam.")
        return()

    cap.set(cv2.CAP_PROP_FPS, max_fps) # fixer les FPS de la cam


    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire l'image.")
            break
        #frame = cv2.resize(frame, (426, 240))
        results = model.predict(frame, imgsz=96)
        #annotated_frame = results.render()[0]
        result_frame = results[0].plot()
        cv2.imshow("YOLO Detection", result_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(model_path='models/yolo11n_ncnn_model_96')