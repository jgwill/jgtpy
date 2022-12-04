#!/bin/bash
versiontype=patch
if [ "$1" != "" ] ; then versiontype=$1;fi
mkdir -p build && \
	json2bash package.json > build/load-package-previous.sh && \
	(npm version $versiontype && git push)|| (echo "Oh, enter commit msg:";read MSG&&git commit . -m "$MSG" && npm version $versiontype  && git push ) && \
	json2bash package.json > build/load-package-upgraded.sh && \
	. build/load-package-previous.sh && export oldversion=$version && \
	. build/load-package-upgraded.sh && export newversion=$version && \
	./_version_sed.sh $oldversion $newversion && \
make dist && \
twine upload dist/*  && echo "Package : $name was published" || echo "Package : $name WAS NOT Published :( "
make clean &> /dev/null
rm -rf build
