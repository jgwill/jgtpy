
# Install ForexConnect in a Python Env above 3.7 for which it was built
# By JGWill, 2023-11-14

SRC_PYTHON_VERSION=3.7

# Where the ForexConnect files are (installed by pip)
CONDA_PY37_ENV_NAME=jgtpy
x=$(conda env list | grep $CONDA_PY37_ENV_NAME)

# Create the env if it does not exist
if [ "$x" == "" ];then 
  conda create -n $CONDA_PY37_ENV_NAME python=$SRC_PYTHON_VERSION --yes
fi

# Activate the env where forexconnect is installed (or will be)
conda activate $CONDA_PY37_ENV_NAME && \
  pip install forexconnect

CONDA_PY37_ENV_DIR=$(echo "$(conda info)" | awk '/active env location/ {print $5}') # Getting our env dir

echo "INFO::Python 3.7 env $CONDA_PY37_ENV_NAME dir is : $CONDA_PY37_ENV_DIR"

# Where the ForexConnect files will be installed (manually) (from conda env above to target env below)
CONDA_PYTARGET_ENV_NAME=jgtpy310
PY_TARGET_VERSION=3.10
export PY_TARGET_VERSION

x=$(conda env list | grep $CONDA_PYTARGET_ENV_NAME)

# Create the env if it does not exist
if [ "$x" == "" ];then 
  conda create -n $CONDA_PYTARGET_ENV_NAME python=$PY_TARGET_VERSION --yes
fi

conda activate $CONDA_PYTARGET_ENV_NAME
export CONDA_TARGET_ENV_DIR=$(echo "$(conda info)" | awk '/active env location/ {print $5}')
echo "Target env $CONDA_PYTARGET_ENV_NAME dir : $CONDA_TARGET_ENV_DIR"

(cd $CONDA_PY37_ENV_DIR/lib/python$SRC_PYTHON_VERSION/site-packages && \
  tar cf - forexconnect* \
    | (cd $(echo "$(conda info)" | awk '/active env location/ {print $5}')/lib/python$PY_TARGET_VERSION/site-packages && \
      tar xvf -) && \
    echo "Done installing forexconnect manually from env:$CONDA_PY37_ENV_NAME to env:$CONDA_PYTARGET_ENV_NAME" ) || \
    echo "ERROR::Failed to install forexconnect manually from env:$CONDA_PY37_ENV_NAME to env:$CONDA_PYTARGET_ENV_NAME"
