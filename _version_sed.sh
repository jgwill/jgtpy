if [ "$2" != "" ]; then
pversion=$1
nversion=$2
cdir=$(pwd)

if [ -e "jgtpy/.flag" ] ;then 
cd jgtpy
for f in $(ls *);do if [ -f "$f" ]; then sed -i 's/'$pversion'/'$nversion'/g' $f &>/dev/null;fi;done
cd $cdir
cd test
for f in $(ls *);do if [ -f "$f" ]; then sed -i 's/'$pversion'/'$nversion'/g' $f &>/dev/null;fi;done
cd $cdir
for f in $(ls *);do if [ -f "$f" ]; then sed -i 's/'$pversion'/'$nversion'/g' $f &>/dev/null;fi;done
else
	echo " MUST USE VM  To have jgtpy Mounted: use dkrun "
fi
else
	echo "Must supply old and new version number"
fi
