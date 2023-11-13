

# Install ForexConnect in a Python Env above 3.7 for which it was built

# Where the ForexConnect files are (installed by pip)
CONDA_PY37_ENV_NAME=jgtpy
conda activate $CONDA_PY37_ENV_NAME && \
  pip install forexconnect

CONDA_ENV_ROOTDIR=~/anaconda3/envs
CONDA_PY37_ENV_DIR=$CONDA_ENV_ROOTDIR/$CONDA_PY37_ENV_NAME

PY_TARGET_ROOT_VERSION_NAME=python3.10
CONDA_PYTARGET_ENV_NAME=tstfxcon

cd $CONDA_PY37_ENV_DIR/lib/python3.7/site-packages && \
  tar cf - forexconnect* \
    | (cd $CONDA_ENV_ROOTDIR/$CONDA_PYTARGET_ENV_NAME/lib/$PY_TARGET_ROOT_VERSION/site-packages/ && \
      tar xvf -) && \
    echo "Done installing manually"
