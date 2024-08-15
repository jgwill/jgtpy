git commit package.json pyproject.toml jgtpy/__init__.py -m bump &>/dev/null
pip install -U jgtutils&>/dev/null && echo "jgtutils upgraded" || echo "jgtutils not installed"
. bump_jgtutils.sh
. scripts/version-patcher.sh
cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
git commit . -m "v$cversion";git tag "$cversion" && git push --tags && git push 

make dist && twine upload dist/* #&& sleep 32 &&  . pypi-conda-gaia-env.sh
echo "pip install -U jgtpy==$cversion"
