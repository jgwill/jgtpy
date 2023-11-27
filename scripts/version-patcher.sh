

if [ -e "package.json" ];then 

pversion=$(cat package.json | grep version | awk -F: '{ print $2 }' | sed 's/[", ]//g')
cversion=""

npm version patch && \
	cversion=$(cat package.json | grep version | awk -F: '{ print $2 }' | sed 's/[", ]//g')

if [ "$cversion" == "" ]; then echo "bahhhh cversion has no value"
else
	echo "Patching files for $cversion from $pversion"
	for f in pyproject.toml jgtpy/JGTCore.py ;do sed -i 's/'$pversion'/'$cversion'/g' $f;done
fi
else echo "Must executer $0 from current directory of package.json"
fi

