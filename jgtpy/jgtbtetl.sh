#!/bin/bash
#--@STCGoal Integrate Strategic Structural Investment Scenario Back-testing to an adequate format for analysing and enhancing algorithmic performance of assistive investment technologies

wdir=$CaishenIndicoreStrategiesDir/standard
scriptdir=$wdir/scripts

#@Example
export BOPFLAG='false'
export bs='Buy'
export fbasename='sigx2211trainV6'
export firstst='11/01/2022 00:00:07'
export instrument='USD/CAD'
export outfile='TST3USD-CAD_m5__Sell__2212082129__2212090005__sigx2211trainV6.json'
export outfn=''
export outfnbase=''
export outprefix='TWN'
export pov='USD/CAD_H1'
export povfn='USD-CAD_H1'
export timeframe='H1'
export tlid='2212100030'
export tlidfirst='2201110000'
export toutputsubdir='output'
#@<<

script_part01=$scriptdir/jgtbtetl1.py
script_part02=$scriptdir/jgtbtetl2.py

echo -n "Loading Context"
. _ctxcurrent.sh
conda activate py372
echo "... context loaded"

tsext="tsv6"
tdir=$wdir/tests
cdir=$(pwd)
tnamespace="$outprefix$povfn-$bs"
tnamespacetlid="$tnamespace-$tlidfirst"
tout=$wdir/$toutputsubdir
ojsonpath=$tout/$outfn
tsfnbase=$povfn"__"$bs
tpath=$tdir/$tnamespacetlid
tsfnbasepath=$tpath/$tsfnbase

tsfn=$tsfnbase"."$tsext
tspath=$tsfnbasepath"."$tsext
jsonenv=$tpath/.env.json
dotenvpath=$tpath/.env

echo "-----------------$tnamespace---------------------"
echo "cd  $tpath  "
echo "-------------------------------------------------"
ctxscriptbasename=_ctxcurrent
ctxscriptsh=$ctxscriptbasename.sh
ctxscriptjson=$ctxscriptbasename.json

mkdir -p $tpath && (cd $tpath ;explorer.exe .)
if [ ! -e "$dotenvpath" ] ; then cp $ctxscriptsh $dotenvpath;fi
if [ ! -e "$tpath/.env.json" ] ; then cp $ctxscriptjson $jsonenv;fi
echo $'\n' >> $dotenvpath
echo "#--------Post env added----" >> $tpath/.env.json
echo "export tnamespace=$tnamespace" >> $dotenvpath
echo "export tnamespacetlid=$tnamespacetlid" >> $dotenvpath
echo "export tsfnbase=$tsfnbase" >> $dotenvpath
echo "export tsfn=$tsfn" >> $dotenvpath
trainfnjson=$tsfn".json"
trainfncsv=$tsfn".csv"
echo "export trainfnjson=$trainfnjson" >> $dotenvpath
echo "export trainfncsv=$trainfncsv" >> $dotenvpath
echo $'\n' >> $dotenvpath
#@STCGoal Well integrated Perspective of Back-Test and CDS Assets
#@STCIssue Having Access to insight on what is an adequate structure to enter - data prepared in that state would bring a perspective
#@a Indicore Saved JSON Traning signal set is transformed in CSV
(cd $tout && pwd && \
echo "Catting and prettying : $outfn" &&  cat $outfn| json > $tspath".json" && \
  echo "Arraying JSON to CSV format in $tpath" && cd $tpath && jsonarr2csv $tspath".json" > $tspath".csv") && \
  echo "A Python has entered the first step of the Pipeline... " && \
(cd $tpath && python $script_part01) && \
echo "ohoh, a Second Python has entered the Pipeline... all is fine " && \
(cd $tpath && python $script_part02)