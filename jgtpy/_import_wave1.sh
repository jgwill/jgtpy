export tdir=$(pwd);(cdpys;ls *PDS*;tar cf - JGTPDS.py JGTPDS.test.py JGTPDS.test.ipynb PDSServicePto2211.cli.py JGTPDHelper.py | (cd $tdir;tar xfv -))
