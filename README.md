# Arbre de Classification - Séparation de Gini

Ce projet est une interface utilisateur construite avec Tkinter en Python pour exécuter des modèles de classification d'arbre basés sur l'indice de Gini.

Ce programme a été fait dans le but de comprendre comment fonctionnait le processus de construction d’un arbre de décision de classification, à l’aide de l’indice de Gini. C’est pour cela, comme indiqué à la suite, qu’il ne fonctionnera que pour les fichiers CSV respectant un certain format.

## Description générale

Le projet est constitué de deux classes principales :

1. `Interface`: Cette classe fournit une interface utilisateur qui permet à l’utilisateur de charger un fichier CSV, puis d’exécuter l’algorithme de classification basé sur l’indice de Gini sur les données importées. L’utilisateur peut visualiser les résultats de la classification directement depuis l’interface.

2. `Gini`: Cette classe implémente l’algorithme de l’arbre de décision basé sur l’indice de Gini. L’algorithme commence par charger les données, puis trouve la meilleure division pour chaque nœud en minimisant cet indice. Cela crée un arbre de décision où chaque nœud contient les individus séparés grâce à une variable et un seuil optimal (dont l’indice de Gini est minimisé) de la branche dont il découle, et chaque feuille de l’arbre correspond à une prédiction de la modalité.

## Comment fonctionne le programme ?

1. Importer un fichier CSV respectant le format spécifique suivant:
   - Il doit contenir au moins deux colonnes.
   - La première colonne doit être nommée 'Y' et contenir uniquement les valeurs 'A' et 'B'.
   - Les autres colonnes doivent contenir uniquement des valeurs numériques.
2. Exécuter un modèle de classification d'arbre basé sur l'indice de Gini.
3. Visualiser le modèle de classification d'arbre.

## Dépendances

Ce projet a besoin des packages Python suivants :
- tkinter
- pandas
- numpy
- PIL (Pillow)
- graphviz
- uuid

Vous pouvez installer ces dépendances avec pip en utilisant la commande suivante:

```bash
pip install tkinter pandas numpy pillow graphviz uuid
```

## Exécution

Pour exécuter ce programme, vous devez d'abord exécuter le script `gini_interface.py`. Voici comment le faire à partir de la ligne de commande :

```bash
python gini_interface.py
```

Vous pouvez également créer un exécutable à partir du script Python en utilisant `pyinstaller` :

```bash
pyinstaller --onefile gini_interface.py
```

L'exécutable sera situé dans le dossier `dist`.

