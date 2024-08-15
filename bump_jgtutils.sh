


# This wont be run by post_dist rather its just a flag to run _bump_jgtutils function




oldjgtutilsversion=$(cat pyproject.toml|grep "jgtutils"|tr '>' ' '|tr "'" " "|tr "=" " "|tr "," " "|awk '{print $2}')
. .env 
(conda activate $WS_CONDA_ENV_NAME&>/dev/null;pip install -U jgtutils|tr '(' ' '|tr ')' ' '|grep "jgtutils in"|awk '/jgtutils/{print $7}')
newjgtutilsversion=$(conda activate $WS_CONDA_ENV_NAME&>/dev/null;pip install -U jgtutils|tr '(' ' '|tr ')' ' '|grep "jgtutils in"|awk '/jgtutils/{print $7}')

# We want to replace jgtutils>=0.4.70 with jgtutils>=0.4.71
## run if they are different
if [ "$oldjgtutilsversion" == "$newjgtutilsversion" ]; then
    echo "No need to update jgtutils version in $WS_CONDA_ENV_NAME package/env"
else

	sed -i "s/jgtutils>=$oldjgtutilsversion/jgtutils>=$newjgtutilsversion/g" pyproject.toml
	git add pyproject.toml
	git commit -m "auto bump:jgtutils  $oldjgtutilsversion to $newjgtutilsversion"
fi


(conda activate baseprod && pip install --user -U jgtutils) &>/dev/null
