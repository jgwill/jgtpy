
cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
git commit . -m "v$cversion" && git tag "$cversion" && git push --tags && git push 
make dist && twine upload dist/* && sleep 15 &&  . pypi-conda-gaia-env.sh