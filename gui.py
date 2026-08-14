import sys
import os
import cv2

from ultralytics import YOLO

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox
)


class ObjectRecognitionApp(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # Fenêtre
        # =========================

        self.setWindowTitle("Object Recognition - YOLO")
        self.setFixedSize(1000, 650)

        # =========================
        # YOLO
        # =========================

        self.model = YOLO("models/yolov8n.pt")

        # =========================
        # Variables
        # =========================

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)

        self.current_image = None
        self.video_path = None

        # =========================
        # Zone image / vidéo
        # =========================

        self.image_label = QLabel("Importer une image ou une vidéo")
        self.image_label.setFixedSize(700, 500)

        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.image_label.setStyleSheet(
            """
            QLabel {
                border: 2px solid #555;
                background-color: #eeeeee;
            }
            """
        )

        # =========================
        # Liste objets
        # =========================

        self.object_list = QListWidget()

        self.object_list.setFixedWidth(240)

        # =========================
        # Boutons
        # =========================

        self.import_button = QPushButton(
            "Importer"
        )

        self.camera_button = QPushButton(
            "Démarrer caméra"
        )

        self.stop_button = QPushButton(
            "Arrêter"
        )

        self.save_button = QPushButton(
            "Enregistrer résultat"
        )

        # =========================
        # Connexions
        # =========================

        self.import_button.clicked.connect(
            self.import_file
        )

        self.camera_button.clicked.connect(
            self.start_camera
        )

        self.stop_button.clicked.connect(
            self.stop_media
        )

        self.save_button.clicked.connect(
            self.save_result
        )

        # =========================
        # Layout image + liste
        # =========================

        display_layout = QHBoxLayout()

        display_layout.addWidget(
            self.image_label
        )

        display_layout.addWidget(
            self.object_list
        )

        # =========================
        # Layout boutons
        # =========================

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.import_button
        )

        button_layout.addWidget(
            self.camera_button
        )

        button_layout.addWidget(
            self.stop_button
        )

        button_layout.addWidget(
            self.save_button
        )

        # =========================
        # Layout principal
        # =========================

        main_layout = QVBoxLayout()

        main_layout.addLayout(
            display_layout
        )

        main_layout.addLayout(
            button_layout
        )

        self.setLayout(
            main_layout
        )

    # ==================================================
    # IMPORTER IMAGE OU VIDEO
    # ==================================================

    def import_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Importer une image ou une vidéo",
            "images",
            """
            Fichiers compatibles
            (*.jpg *.jpeg *.png *.bmp
             *.mp4 *.avi *.mov *.mkv)
            """
        )

        if not filename:
            return

        # Arrêter une éventuelle caméra/vidéo
        self.stop_media()

        extension = os.path.splitext(
            filename
        )[1].lower()

        # =========================
        # IMAGE
        # =========================

        image_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp"
        ]

        if extension in image_extensions:

            self.load_image(filename)

        # =========================
        # VIDEO
        # =========================

        else:

            self.load_video(filename)

    # ==================================================
    # CHARGER IMAGE
    # ==================================================

    def load_image(self, filename):

        image = cv2.imread(filename)

        if image is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Impossible de charger cette image."
            )

            return

        # YOLO
        results = self.model(image)

        # Image annotée
        result_image = results[0].plot()

        self.current_image = result_image.copy()

        # Afficher
        self.display_image(
            result_image
        )

        # Liste objets
        self.update_object_list(
            results
        )

    # ==================================================
    # CHARGER VIDEO
    # ==================================================

    def load_video(self, filename):

        self.cap = cv2.VideoCapture(
            filename
        )

        if not self.cap.isOpened():

            QMessageBox.warning(
                self,
                "Erreur",
                "Impossible d'ouvrir cette vidéo."
            )

            self.cap = None

            return

        self.video_path = filename

        # Lecture vidéo
        self.timer.start(30)

    # ==================================================
    # CAMERA
    # ==================================================

    def start_camera(self):

        self.stop_media()

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():

            QMessageBox.warning(
                self,
                "Erreur",
                "Impossible d'ouvrir la caméra."
            )

            self.cap = None

            return

        self.timer.start(30)

    # ==================================================
    # VIDEO / CAMERA
    # ==================================================

    def update_video(self):

        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:

            self.stop_media()

            return

        # YOLO
        results = self.model(frame)

        # Dessiner les résultats
        result_frame = results[0].plot()

        self.current_image = result_frame.copy()

        # Afficher
        self.display_image(
            result_frame
        )

        # Liste objets
        self.update_object_list(
            results
        )

    # ==================================================
    # LISTE DES OBJETS
    # ==================================================

    def update_object_list(self, results):

        self.object_list.clear()

        detected_objects = {}

        for box in results[0].boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            object_name = self.model.names[
                class_id
            ]

            confidence_percent = (
                confidence * 100
            )

            self.object_list.addItem(
                f"{object_name} - "
                f"{confidence_percent:.1f}%"
            )

            # Compteur
            if object_name not in detected_objects:

                detected_objects[
                    object_name
                ] = 0

            detected_objects[
                object_name
            ] += 1

    # ==================================================
    # AFFICHER IMAGE
    # ==================================================

    def display_image(self, image):

        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        height, width, channel = (
            rgb_image.shape
        )

        bytes_per_line = (
            channel * width
        )

        qt_image = QImage(
            rgb_image.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(
            qt_image
        )

        scaled_pixmap = pixmap.scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(
            scaled_pixmap
        )

    # ==================================================
    # ARRETER
    # ==================================================

    def stop_media(self):

        self.timer.stop()

        if self.cap is not None:

            self.cap.release()

            self.cap = None

    # ==================================================
    # ENREGISTRER RESULTAT
    # ==================================================

    def save_result(self):

        if self.current_image is None:

            QMessageBox.information(
                self,
                "Information",
                "Aucun résultat à enregistrer."
            )

            return

        os.makedirs(
            "results",
            exist_ok=True
        )

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le résultat",
            "results/result.jpg",
            "Image JPEG (*.jpg);;Image PNG (*.png)"
        )

        if not filename:
            return

        cv2.imwrite(
            filename,
            self.current_image
        )

        QMessageBox.information(
            self,
            "Enregistrement",
            "Résultat enregistré avec succès."
        )

    # ==================================================
    # FERMETURE
    # ==================================================

    def closeEvent(self, event):

        self.stop_media()

        event.accept()


# ======================================================
# LANCEMENT
# ======================================================

app = QApplication(sys.argv)

window = ObjectRecognitionApp()

window.show()

sys.exit(
    app.exec()
)