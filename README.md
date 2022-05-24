# PLDAC

## Génération des tags

    Le dossier generation_qrcode contient les fonctions qui ont permit la génération des tags.
    La version finale des tags est dans le fichier 'out/qr_codes2outlinev?.svg'

## Détection des tags

	Lancer main.py

	Pour tester avec d'autres images :
		- changer le chemin (images disponibles dans le dossier images_tests)
		- attention à l'aire si on utilise d'autres images que celles des fourmis (voir commentaire ligne 43-44 de detection.py)
    
    analyse_qr.py permet la traduction des Qr_codes (sous forme de matrice bianire) en identifiant
    detection.py permet la detection depuis une image des QR_codes et la traduction en matrice binaire

## Modeles d'analyse des réseaux d'interactions

    Le jupyter notebook modeles.ipynb permet de tester les différents modèles de classifications de rôles des fourmis et d'études des intéractions.
    Ce jupyter appelle les fonctions des fichiers .py du dossier modeles