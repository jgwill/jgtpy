cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
conda activate jgtpy-pypi && sleep 1 && echo "... Waiting before we install the fresh package $cversion" && sleep 1 && echo "..." && \
	pip uninstall -y jgtpy && sleep 2 && \
	echo "pip install jgtpy==$cversion" && sleep 1 && pip install -U jgtpy==$cversion && \
	echo "------ New version should be installed ----" && \
	echo " Entering ./test" && \
	cd test && ls *py *sh 
	(sleep 10;pip install -U jgtpy==$cversion &>/dev/null) &
	
