#

for f in *.txt ;
do
	if [ -e  "../paroles/$f" ] ; then
		echo DOUBLON $f
		diff -q "$f" "../paroles/$f"
	fi
done
