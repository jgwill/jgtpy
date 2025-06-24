git commit package.json pyproject.toml jgtpy/__init__.py -m bump &>/dev/null

. /opt/binscripts/load.sh 
make bump_jgtutils
. scripts/version-patcher.sh
cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
git commit . -m "v$cversion";git tag "$cversion" && git push --tags && git push 

make dist && twine upload dist/* #&& sleep 32 &&  . pypi-conda-gaia-env.sh
echo "pip install --user -U jgtpy==$cversion"
