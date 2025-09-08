#

# Convertit des documents en png
# et les mets dans le répertoire des partitions

# Usage :   ./convertir.sh   truc.odt machin.odt

PARTITIONS=../docs/partitions
libreoffice --convert-to png --outdir ${PARTITIONS} $*
