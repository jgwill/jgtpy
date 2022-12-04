#!/bin/bash
. _env.sh
mkdir -p logs

if [ "$HOSTNAME" != "$dkhostname" ]; then
#. build-by-docker.sh
	 echo "Launching DockerTAG: $dockertag to build and publish "
	dkrun "bash /work/build-n-release.sh" || $binroot/dkrun "bash /work/build-n-release.sh"
  #bash -c '. $HOME/.bashrc && dkrun "bash /work/build-n-release.sh"'
else

#logfile=build-log.txt
versiontype=patch
if [ "$1" != "" ] ; then versiontype="$1";fi
if [ -e "build/build-flag" ];then rm -rf build;fi

mkdir -p build && echo "building" > build/build-flag && \
	json2bash package.json . -x > build/load-package-previous.sh && \
	. build/load-package-previous.sh && export oldversion="$version" && export _continue="1" || export _continue="0"
#export _continue="0"
if [ "$_continue" == "0" ];then
	msg="Failed getting old version - maybe json2bash...."
	echo "$msg";echo "$msg" >> $logfile
else
npm version $versiontype > build/npm-version-out.txt && git push|| (echo "Oh, enter commit msg:";read MSG&&git commit . -m "$MSG" && npm version $versiontype  && git push )  &&  export _continue="1" || export _continue="0"

if [ "$_continue" == "0" ];then
        msg="Failed with version upping"
        echo "$msg";echo "$msg" >> $logfile
else
	json2bash package.json . -x  > build/load-package-upgraded.sh && \
	. build/load-package-upgraded.sh && export newversion="$version" && export _continue="1" || export _continue="0"

if [ "$_continue" == "0" ];then
        msg="Failed getting new version with json2bash"
        echo "$msg";echo "$msg" >> $logfile
else

chmod a+x _version*sh
./_version_sed.sh "$oldversion" "$newversion" && echo "Upped $versiontype $oldversion > $newversion"  >> $logfile && \
make dist && \
twine upload dist/*  && echo "Package : $name was published" || echo "Package : $name WAS NOT Published :( "
make clean &> /dev/null
#rm -rf build


fi

fi

fi

fi
