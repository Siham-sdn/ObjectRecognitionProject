from ultralytics import YOLO
import cv2

# Charger le modèle YOLO
model = YOLO("model/yolov8n.pt")

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : impossible d'ouvrir la caméra")
    exit()

while True:
    # Lire une image de la caméra
    ret, frame = cap.read()

    if not ret:
        print("Erreur de lecture caméra")
        break

    # Détection YOLO
    results = model(frame)

    # Dessiner les résultats
    annotated_frame = results[0].plot()

    # Afficher la vidéo
    cv2.imshow("YOLO Detection - Camera", annotated_frame)

    # Quitter avec la touche q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Libérer la caméra
cap.release()
cv2.destroyAllWindows()