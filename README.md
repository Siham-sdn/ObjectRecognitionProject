# Object Recognition Project 🤖

## Description

**Object Recognition Project** est une application desktop développée en **Python** permettant la **détection et la reconnaissance d’objets sur des images, des vidéos et des flux webcam en temps réel**.

L’application utilise le modèle **YOLO** pour effectuer la détection des objets et **OpenCV** pour le traitement et l’acquisition des images et vidéos. Une interface graphique développée avec **PyQt6** permet à l’utilisateur d’importer des médias, d’afficher les résultats de détection et d’enregistrer les résultats.

## Prérequis

Pour exécuter le projet, il vous faut :

- **Python 3.x**
- **pip**
- Un environnement virtuel Python (`venv`)
- Une webcam pour utiliser la détection en temps réel
- Les bibliothèques Python nécessaires listées dans `requirements.txt`
- Un modèle **YOLO** (`yolov8n.pt`)

### Bibliothèques utilisées

- **Ultralytics / YOLO**
- **OpenCV**
- **PyQt6**
- **NumPy**

## Fonctionnalités principales

- Chargement d’images
- Chargement de vidéos
- Capture vidéo via **Webcam**
- Détection d’objets avec **YOLO**
- Détection en temps réel
- Affichage des cadres autour des objets détectés
- Affichage du nom des objets détectés
- Affichage du niveau de confiance (%)
- Liste des objets détectés
- Analyse de vidéos image par image
- Sauvegarde des résultats
- Interface graphique développée avec **PyQt6**

### Types de médias supportés

**Images :**
- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`

**Vidéos :**
- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

## Interface de l'application

L’interface est composée de :

<img width="960" height="540" alt="Interface YOLO" src="URL_DE_TA_CAPTURE_ICI" />

- **Zone d’affichage centrale** : affichage des images, vidéos et flux webcam
- **Zone des objets détectés** : affichage des classes détectées et de leur niveau de confiance
- **Bouton Importer** : importation d’une image ou d’une vidéo
- **Bouton Démarrer caméra** : activation de la webcam
- **Bouton Arrêter** : arrêt de la caméra ou de la vidéo
- **Bouton Enregistrer résultat** : sauvegarde du résultat de la détection

## Fonctionnement

Le traitement des médias suit le principe suivant :

```text
Image / Vidéo / Webcam
          ↓
        OpenCV
          ↓
      Modèle YOLO
          ↓
  Détection des objets
          ↓
 ┌─────────────────────┐
 │ Classe de l'objet   │
 │ Cadre de détection  │
 │ Confiance (%)       │
 └─────────────────────┘
          ↓
      Interface PyQt6
          ↓
    Affichage du résultat


## Installation & exécution
# Cloner le dépôt
git clone https://github.com/VOTRE-NOM/ObjectRecognitionProject.git

# Accéder au projet
cd ObjectRecognitionProject

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel sous Windows
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python gui.py

## Modèle YOLO:
Le projet utilise le modèle **YOLOv8n** et il doit être placé dans le dossier **models**

## Chemins
/ (root)
  ├── gui.py
  ├── main.py
  ├── camera_detection.py
  ├── requirements.txt
  ├── README.md
  │
  ├── models/
  │   └── yolov8n.pt
  │
  ├── images/
  │   └── Images et vidéos de test
  │
  └── results/
      └── Résultats des détections
