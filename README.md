# live-karaoke.github.io

Pour ajouter une chanson:
- créer un fichier ma_chanson.txt avec 4 champs: titre, artist, youtube, partition, tabs.
  - tabs et youtube sont optionnels.
  - partition indique le fichier image (png) contenant la grille.
```
titre: La symphonie des éclairs
artist: Zaho de Sagazan
youtube: https://www.youtube.com/watch?v=pqo59FkF_5g
partition: la_symphonie_des_eclairs.png
tabs: https://tabs.ultimate-guitar.com/tab/4711379
paroles:
Il fait toujours beau au-dessus des nuages
Mais moi, si j'étais un oiseau, j'irais danser sous l'orage
Je traverserais les nuages comme le fait la lumière
J'écouterais sous la pluie la symphonie des éclairs
```
Le fichier ma_chanson.txt doit être placé dans le répertoire 'paroles'. Ensuite il faut créer un fichier image de type png contenant la grille (idéalement 1 page seulement) et le placer dans 'docs/partitions'. Le nom de ce fichier doit figurer dans le champs 'partition' du fichier texte.

Ensuite lancer la moulinette:
```
python moulinette.py
```
et publier le tout:
```
./publish.sh
```

c'est prêt :)
