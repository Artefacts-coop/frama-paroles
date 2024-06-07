# How-to


## Génération de fausses données

Lancer la commande suivante 
```bash
python3 outils/generate_fake_data.py
```

Le fichier `fake_data.sqlite`est généré.


## Base de données anonymisée

Cette anonymisation consiste principalement à supprimer les informations personnelles.

Lancer la commande suivante 
```bash
python3 outils/anonymize.py <chemin/vers/le/fichier.sqlite>
```

Le fichier anonymisé `data.sqlite`est généré.