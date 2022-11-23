pversion=0.1.3
nversion=0.1.4
cdir=$(pwd)

cd jgtpy
for f in $(ls *);do sed -i 's/'$pversion'/'$nversion'/g' $f &>/dev/null;done
cd $cdir
cd test
for f in $(ls *);do sed -i 's/'$pversion'/'$nversion'/g' $f &>/dev/null;done
cd $cdir
for f in $(ls *);do sed -i 's/'$pversion'/'$nversion'/g' $f &>/dev/null;done

