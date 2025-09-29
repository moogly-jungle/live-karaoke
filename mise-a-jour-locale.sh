#!/bin/bash -x

# génération des fichiers localement
# - ne s'occupe pas du git
# - ni de la publication
# lance firefox pour pouvoir vérifier

(
	cd sources-partitions
	./convertir_nouvelles_partitions.sh
)
python3 verifier-paroles.py
# python3 moulinette.py

rm docs/paroles/*.html
python3 nouvelle-moulinette.py
./compiler-liste-latex.sh

rm latex/liste.*

#
firefox file:docs &
