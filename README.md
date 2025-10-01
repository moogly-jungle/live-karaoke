# live-karaoke.github.io

## Pour ajouter une chanson:

- créer un fichier ma_chanson.txt avec 4 champs: 
`titre`, `artiste`, `youtube`, `partition`, `tabs`.

- les champs `tabs` et `youtube` sont optionnels.
- partition indique le fichier image (PNG ?) contenant la grille et la structure
  
Exemple :

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

Le fichier `ma_chanson.txt` doit être placé dans le répertoire
`paroles/`.  Ensuite il faut créer un fichier image (de type PNG)
contenant la grille (idéalement 1 page seulement) et le placer dans
`docs/partitions/`. Le nom de ce fichier doit figurer dans le champ
`partition:[ du fichier texte.

# Pour mettre à jour le site

1. lancer le script `mise-a-jour-locale.sh`, qui fera tourner la
moulinette et produira les divers fichiers HTML, PDF etc. aux endroits
voulus.


```
$ ./mise-a-jour-locale.sh
```
ce script lance aussi `firefox` sur l'arborescence locale, ce
qui permet de vérifier que la génération des fichiers s'est bien passée.

2. mettre à jour le dépôt `git`, valider les ajouts/retraits/modifications

3. et publier le tout:

```
$ ./publish.sh
```

c'est prêt :)



# Doc de la moulinette

Le code de la moulinette a été revus pour utiliser des templates, ce 
qui simplifie énormément la production de documents de formats divers.

Le moteur de templates utilisé est `jinja2`.

Le format des fichiers a été revu aussi, il ressemble au format des mails

## Format des fichiers de chansons

Un fichier "chanson" par un entête, suivi par le corps avec les paroles.

Chaque ligne de l'entête contient un "tag", suivi par le caractère ":"
et une chaine de caractères.

L'entête est séparé du corps par une ligne blanche (comme les mails),
ou par le tag "`paroles:`" ou "`lyrics:`" par mesure de compatibilité
avec le format initial)

Les tags permis / obligatoires sont indiqués ci-dessous, avec des
synonymes en français

(extrait du fichier `songfilereader.py`)

~~~python
allowed_tags  = ['title', 'score', 'artist', 'youtube', 'tabs', 'lyrics']
required_tags = ['title', 'artist', 'score' ]

tag_aliases = {
    'titre': 'title',
    'artiste': 'artist',
    'partition': 'score',
    'paroles': 'lyrics'
}
~~~
