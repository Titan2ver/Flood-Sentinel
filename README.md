# Flood Sentinel : station de prévention des inondations

Station de mesure autonome, basée sur un Raspberry Pi 4, qui surveille un cours
d'eau pour anticiper les crues. Le cœur du projet est un module de vision : une
webcam filme la surface de la rivière, et le flux optique entre les images
successives permet d'estimer la vitesse de l'écoulement.

Projet de fin d'année E3T à l'ESIEE Paris, réalisé en équipe.

![Flux optique sur une vidéo de crue](images/optical_flow.png)

## Architecture

- **Raspberry Pi 4** avec carte d'extension à borniers
- **Webcam** : mesure de la vitesse de surface par traitement d'image
- **Capteurs étudiés** : niveau d'eau, débit, ultrasons (HC-SR04), lidar
- **Interface** : tableau de bord Node-RED et page web servie par Apache

## Mesure de vitesse par flux optique

1. Enregistrement d'une séquence de 2 s avec la webcam, toutes les 10 s
2. Calcul du flux optique dense (algorithme de Farneback, OpenCV)
3. Moyenne de l'amplitude du mouvement sur une ligne qui traverse la rivière,
   puis conversion en m/s avec un facteur d'étalonnage
4. Ajout des valeurs dans un fichier CSV et génération des graphiques
5. Publication de la dernière image et des graphiques sur la page web

| Profil de vitesse le long de la rivière | Vitesse au cours du temps |
|---|---|
| ![](docs/images/speed_profile.png) | ![](docs/images/speed_time.png) |

Le profil montre un écoulement plus rapide au centre du lit (jusqu'à environ 6 m/s)
et quasi nul près des berges.

## Limites

L'amplitude du flux est normalisée à chaque image, et l'étalonnage pixel vers
mètre est approximatif. Les vitesses obtenues sont donc des estimations
relatives. Pour une mesure absolue, il faudrait étalonner la caméra sur un
objet de dimensions connues, placé à la surface de l'eau.

## Lancer le projet

    pip install -r requirements.txt
    python src/video_flow_view.py        # visualisation sur samples/rec.avi
    python src/live_flow_view.py         # visualisation en direct (webcam)

## Technologies

Python · OpenCV · NumPy · Matplotlib · Raspberry Pi · Node-RED · Apache