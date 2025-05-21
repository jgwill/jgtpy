
. $HOME/.bashrc&>/dev/null

(cd ../jgtml && . upjgtpy_version.sh)


postdistpyproject_arch() {

if [ ! -e pyproject.toml ];then
	echo "No pyproject.toml file found. Not a python project?"
else

	current_package_name=$(cat pyproject.toml |grep name|head -n 1 -|tr '"' ' '|awk '{print $3}')
	. .env||echo "No .env file found. Assuming that is fine"
	#foreach $WS_CONDA_ENV_DEPENDING if it exists
	if [ -z "$WS_CONDA_ENV_DEPENDING" ];then
		echo "No WS_CONDA_ENV_DEPENDING found. Assuming that is fine but what can we do... define it in .env file"
		echo "WS_CONDA_ENV_DEPENDING=\"myenv1 myenv2\""
	else
		echo "WS_CONDA_ENV_DEPENDING found. Checking if all environments are installed"
		
		for myenv in $WS_CONDA_ENV_DEPENDING;do
			echo -n "upgrading $current_package_name in $myenv environment..."
			(conda activate $myenv&>/dev/null && pip install -U $current_package_name&>/dev/null && echo "updated with package $current_package_name" || echo " not found or pip install -U $current_package_name failed")
		done
	fi
fi
}

postdistpyproject
