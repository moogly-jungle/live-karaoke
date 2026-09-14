#!/usr/bin/env python3


# Objectif
# verifier les fichiers paroles/*.txt

# Controles
# - le nom du fichier se termine par ".txt"
# - le fichier est lisible par la moulinette
#    (tags connus, tags obligatoires présents)
# - le tag partition correspond à un fichier existant dans docs/partitions
# - le lien youtube contient un identifiant de vidéo valide

import os
import re

from songfilereader import SongFileReader

# un identifiant de vidéo YouTube fait 11 caractères (lettres, chiffres, - et _)
youtube_regex = re.compile(
    r'https?://(youtu\.be/|(www\.|m\.)?youtube\.com/watch\?(.*&)?v=)'
    r'[A-Za-z0-9_-]{11}([?&#].*)?')

def erreurs_chanson(song):
    """ Renvoie la liste des erreurs trouvées dans l'entête d'une chanson."""
    erreurs = []
    nom_partition = song.header['score']
    if nom_partition == "":
        erreurs.append("champ 'partition' vide")
    elif not os.path.exists(f"docs/partitions/{nom_partition}"):
        erreurs.append(f"'{nom_partition}' n'existe pas dans docs/partitions")
    youtube = song.header.get('youtube')
    if youtube is not None and not youtube_regex.fullmatch(youtube):
        erreurs.append(f"lien youtube invalide '{youtube}'")
    return erreurs

reader = SongFileReader()
nb_fichiers_ok = 0
nb_fichiers_ko = 0

for nom in sorted(os.listdir("paroles")):
    if not nom.endswith('.txt'):
        nb_fichiers_ko += 1
        print(f"ERREUR: {nom} n'est pas un fichier .txt")
        continue
    song = reader.read_from(f"paroles/{nom}")
    if song is None:
        # l'erreur a déjà été affichée par le reader
        nb_fichiers_ko += 1
        continue
    erreurs = erreurs_chanson(song)
    for erreur in erreurs:
        print(f"ERREUR: {nom}\t{erreur}")
    if erreurs:
        nb_fichiers_ko += 1
    else:
        nb_fichiers_ok += 1

print(f"Fichiers OK: {nb_fichiers_ok}")
print(f"Fichiers KO: {nb_fichiers_ko}")
