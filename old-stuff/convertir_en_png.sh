#!/bin/bash

# Convertit des documents en png
# et les met dans le répertoire des partitions

PARTITIONS=../docs/partitions

# Usage :   ./convertir.sh  f1 f2 ...

if [ $# == 0 ] ; then
	echo "Usage :   $0  f1 f2 ..." >&1
else
	libreoffice --view --convert-to png --outdir ${PARTITIONS} "$@"
fi
