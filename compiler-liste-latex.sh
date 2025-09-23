#

# compile la liste  en mlatex et met le pdf dans /docs

if ! which -s xelatex ; then
	cat <<AAA
ALERTE
cho on a besoin de la commande xelatex
pour compiler le source.
(package texlive de debian)
AAA
	exit 1
fi

if [ ! -r latex/liste.tex ] ; then
cat <<AAA
ALERTE
le fichier latex/liste.tex
n'a pas été fabriqué
(relancer la moulinette ?)
AAA
	exit 1
fi

(cd latex ; xelatex liste.tex)
mv latex/liste.pdf docs

