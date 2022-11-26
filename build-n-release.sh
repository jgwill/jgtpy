#!/bin/bash
mkdir -p build && \
	json2bash package.json > build/load-package-previous.sh && \
	npm version patch || (git commit .  && \ 
	npm version patch) && \
	json2bash package.json > build/load-package-upgraded.sh && \
	. build/load-package-previous.sh && export oldversion=$version && \
	. build/load-package-upgraded.sh && export newversion=$version && \
	./_version_sed.sh $oldversion $newversion && \
make dist && \
twine upload dist/*  && echo "Package : $name was published" || echo "Package : $name WAS NOT Published :( "
make clean &> /dev/null
rm -rf build
