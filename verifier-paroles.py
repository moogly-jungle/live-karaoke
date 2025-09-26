#!/usr/bin/env python3


# Objectif
# verifier les fichiers paroles/*.txt

# Controles
# - le nom du fichier se termine par ".txt"
# - le tag partition est présent
#    et correspond à un fichier existant dans docs/partitions

import os

paroles = os.listdir("paroles")
nb_fichiers_ok = 0
nb_fichiers_ko = 0

for nom in paroles:
    if not nom.endswith('.txt'):
        nb_fichiers_ko += 1
        print(f"ERREUR: {nom} n'est pas un fichier .txt")
        continue
    with open(f"paroles/{nom}") as f: 
        tag = "partition"
        tag_found = False
        for line in f:
           if line.startswith(tag + ':'):
                tag_found = True
                nom_partition = line[(len(tag) + 1):].strip()
                if nom_partition == "":
                    print(f"ERREUR: {nom}\tchamp 'partition' vide")
                    nb_fichiers_ko += 1
                    break
                chemin_partition = f"docs/partitions/{nom_partition}"
                if os.path.exists(chemin_partition):
                    nb_fichiers_ok += 1
                else:
                    print(f"ERREUR: {nom}\t'{nom_partition}' n'existe pas dans docs/partitions")
                    nb_fichiers_ko += 1
                break
        if not tag_found:
            nb_fichiers_ko += 1 
            print(f"ERREUR: pas de tag 'partition' dans {nom}")

print(f"Fichiers OK: {nb_fichiers_ok}")
print(f"Fichiers KO: {nb_fichiers_ko}")
