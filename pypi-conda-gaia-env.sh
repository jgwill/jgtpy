cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
conda activate jgtpy-pypi && sleep 1 && echo "... Waiting before we install the fresh package $cversion" && sleep 2 && echo "..." && sleep 4 && \
	pip uninstall -y jgtpy && \
	echo "pip install -U jgtpy==$cversion" && sleep 1 && pip install -U jgtpy==$cversion && \
	echo "------ New version should be installed ----" && \
	echo " Entering ./test" && \
	cd test && ls *py *sh 
	
