import cv2

def test_webcam():
    # Ouvrir la webcam (0 est généralement l'index de la caméra par défaut)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam.")
        return

    print("Appuyez sur 'q' pour quitter.")

    while True:
        # Lire une frame de la webcam
        ret, frame = cap.read()

        if not ret:
            print("Erreur : Impossible de lire la frame.")
            break

        # Afficher la frame
        cv2.imshow('Webcam', frame)

        # Quitter si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_webcam()
