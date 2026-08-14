from ultralytics import YOLO
import cv2

# Charger le modèle YOLO
model = YOLO("model/yolov8n.pt")
# Charger une image de test
image = cv2.imread("image/image_test.jpg")
# Détection
results = model(image)

# Afficher le résultat
annotated_image = results[0].plot()

cv2.imshow("Detection YOLO", annotated_image)

cv2.waitKey(0)
cv2.destroyAllWindows()