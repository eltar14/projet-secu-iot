import cv2
"""
Fichier pour tester le fonctionnement de la lib cv2.
Va afficher l'image puis sa version niveaux de gris
"""

image = cv2.imread('4.2.05.tiff')

if image is None:
    print("Erreur : Impossible de charger l'image.")
else:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Afficher l'image originale et l'image en niveaux de gris
    cv2.imshow('Original', image)
    cv2.imshow('Grayscale', gray_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
