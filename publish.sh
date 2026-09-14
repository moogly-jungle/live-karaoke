#!/bin/bash

# Publication du site : main -> production (branche servie par GitHub Pages)
#
# Se lance depuis main ou depuis production, et reste sur cette branche :
# 1. on y fusionne ce que les autres ont publié (main et production
#    sur GitHub, et l'autre branche locale)
# 2. on vérifie qu'il ne reste pas de marqueurs de conflit dans le site
# 3. on envoie le résultat sur main et sur production (GitHub),
#    puis on aligne l'autre branche locale
#
# En cas de problème, le script s'arrête et affiche la marche à suivre.

# Tout le script est entre { } : bash le lit en entier avant de
# l'exécuter, ce qui évite les surprises quand une fusion remplace
# ce fichier pendant qu'il tourne.
{

set -e

etape="vérifications"

fusion_en_cours() {
	git rev-parse -q --verify MERGE_HEAD > /dev/null
}

aide_conflit() {
	cat <<AAA

Il y a un CONFLIT : les mêmes lignes ont été modifiées des deux côtés.
Marche à suivre (sans changer de branche) :

  1. voir les fichiers en conflit (lignes "both modified") :
       git status

  2. dans chaque fichier, garder la bonne version et supprimer
     les lignes de marqueurs <<<<<<< ======= >>>>>>>
     (pour un fichier docs/chansons/*.html : corriger plutôt
     le fichier de paroles/, puis relancer ./mise-a-jour-locale.sh)

  3. marquer chaque fichier corrigé :
       git add nom_du_fichier

  4. terminer la fusion et relancer la publication :
       git commit --no-edit
       ./publish.sh

Pour tout annuler et revenir à l'état d'avant :
       git merge --abort
AAA
}

# appelé automatiquement quand une commande échoue
en_cas_d_erreur() {
	echo
	echo "ERREUR pendant l'étape : $etape"
	if fusion_en_cours ; then
		aide_conflit
		return
	fi
	case "$etape" in
	récupération*|envoi*)
		cat <<AAA

Causes possibles : pas de connexion internet, problème de droits
sur GitHub, ou quelqu'un a publié au même moment.
Marche à suivre :

  1. vérifier la connexion
  2. relancer la publication :
       ./publish.sh
AAA
		;;
	*)
		cat <<AAA

Le message de git juste au-dessus explique le problème.
En cas de doute, ne rien modifier et demander de l'aide.
AAA
		;;
	esac
}
trap en_cas_d_erreur ERR

# ---- vérifications avant de commencer ---------------------------------

if fusion_en_cours ; then
	echo "ALERTE : une fusion a été commencée mais pas terminée."
	aide_conflit
	exit 1
fi

modifs=$(git status --porcelain --untracked-files=no)
nouveaux=$(git status --porcelain -- paroles docs sources-partitions templates | grep '^??' || true)
if [ -n "$modifs$nouveaux" ] ; then
	echo "ALERTE : ces fichiers sont modifiés ou nouveaux, mais pas commités :"
	printf '%s\n%s\n' "$modifs" "$nouveaux" | grep -v '^$' | sed 's/^/    /'
	cat <<AAA

Marche à suivre :

  1. ajouter les nouveaux fichiers du site :
       git add paroles docs sources-partitions templates

  2. commiter, avec un message qui décrit le changement :
       git commit -am "Ajout de la chanson ..."

  3. relancer la publication :
       ./publish.sh

Si ces modifications ne doivent pas encore être publiées :
       git stash -u
       ./publish.sh
       git stash pop
AAA
	exit 1
fi

branche=$(git branch --show-current)
case "$branche" in
main)       autre=production ;;
production) autre=main ;;
*)
	cat <<AAA
ALERTE : ce script se lance depuis la branche main ou production
(branche actuelle : ${branche:-aucune}).
Marche à suivre :

       git checkout main
       ./publish.sh
AAA
	exit 1
	;;
esac

# ---- récupération de ce que les autres ont publié ---------------------

etape="récupération des nouveautés sur GitHub"
git fetch origin

etape="fusion de main (GitHub) dans $branche"
git merge --no-edit origin/main

etape="fusion de production (GitHub) dans $branche"
git merge --no-edit origin/production

if git rev-parse -q --verify "refs/heads/$autre" > /dev/null ; then
	etape="fusion de la branche $autre locale dans $branche"
	git merge --no-edit "$autre"
fi

# ---- pas de marqueurs de conflit oubliés ------------------------------

etape="recherche de marqueurs de conflit"
if git grep -n -I -E '^(<<<<<<<|>>>>>>>)( |$)|^=======$' -- paroles docs templates ; then
	cat <<AAA

ALERTE : les lignes ci-dessus sont des marqueurs de conflit git
oubliés. Ils s'afficheraient tels quels sur le site.
Marche à suivre :

  1. ouvrir chaque fichier indiqué, garder la bonne version
     et supprimer les lignes <<<<<<< ======= >>>>>>>
     (pour un fichier docs/chansons/*.html : corriger plutôt
     le fichier de paroles/, puis relancer ./mise-a-jour-locale.sh)

  2. commiter la correction :
       git commit -am "Suppression des marqueurs de conflit"

  3. relancer la publication :
       ./publish.sh
AAA
	exit 1
fi

# ---- publication -------------------------------------------------------

etape="envoi de $branche vers main sur GitHub"
git push origin "$branche:main"

etape="envoi de $branche vers production sur GitHub"
git push origin "$branche:production"

# l'autre branche locale est déjà incluse dans celle-ci : on l'aligne
etape="mise à jour de la branche $autre locale"
git branch -f "$autre" "$branche"

echo
echo "Publication terminée : $(git log -1 --format='%h %s')"
echo "Le site sera à jour d'ici quelques minutes."
exit 0
}
