cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
conda activate jgtpy-pypi && sleep 2 && \
	pip uninstall -y jgtpy && \
	pip install -U jgtpy==$cversion && \
	echo "------ New version should be installed ----" && \
	echo " Entering ./test" && \
	cd test && ls *py || \
	pip install -U jgtpy==$cversion && \
	        echo "------ New version should be installed ----" && \
		        echo " Entering ./test" && \
			        cd test && ls *py *sh


