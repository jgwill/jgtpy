oldjgtpyversion=$(cat pyproject.toml|grep "jgtpy"|tr '>' ' '|tr "'" " "|tr "=" " "|tr "," " "|awk '{print $2}')
(conda activate jgtml&>/dev/null;pip install -U jgtpy|tr '(' ' '|tr ')' ' '|grep "jgtpy in"|awk '/jgtpy/{print $7}')
newjgtpyversion=$(conda activate jgtml&>/dev/null;pip install -U jgtpy|tr '(' ' '|tr ')' ' '|grep "jgtpy in"|awk '/jgtpy/{print $7}')

# We want to replace jgtpy>=0.4.70 with jgtpy>=0.4.71
## run if they are different
if [ "$oldjgtpyversion" == "$newjgtpyversion" ]; then
    echo "No need to update jgtpy version in jgtml package"
else

	sed -i "s/jgtpy>=$oldjgtpyversion/jgtpy>=$newjgtpyversion/g" pyproject.toml
	git add pyproject.toml
	git commit -m "Updated jgtpy version from $oldjgtpyversion to $newjgtpyversion"
fi
