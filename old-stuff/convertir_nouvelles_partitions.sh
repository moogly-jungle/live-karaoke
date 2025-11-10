#

# convertit en .png tous les sources .odt ou .odg
# de ce répertoir de ce qui en ont besoin
# - si absent de ../docs/partitions
# - ou présent mais pas à jour (le png est plus vieux que le source)

# Attention : dans le for, si il n'y a pas de .odg (ou .odt)
# dans le répertoire,
# *.odg s'expanse en "*.odg" et c'est pas un fichier.
# d'où la précaution.
# il doit y avoir une option du shell pour éviter cette expansion,
# mais j'ai la flemme de chercher.

png_dir=../docs/partitions

for suffixe in odt odg ; do 
	for source_file in *.$suffixe ;  do
		 if [ ! -e "$source_file" ] ; then
	        continue   # Précaution
	     fi
		 prefixe=$(basename "$source_file" .$suffixe)
		 png_file="${png_dir}/${prefixe}.png"

		 if [ ! -e "${png_file}" ] ; then
			 echo "${png_file}" ABSENT
			 ./convertir_en_png.sh "${source_file}"
		 elif test  "${png_file}" -ot "${source_file}"   ; then
			 echo "${png_file}" PAS A JOUR
			 ./convertir_en_png.sh "${source_file}"
		 fi
	done	 
done
