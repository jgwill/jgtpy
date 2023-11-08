#dockertag=jgwill/ubuntu:18.04-py3.7.2-ml-lzma-builder
dockertag=jgwill/server:python-package-builder
containername=jgtapybuilder

export logfile=logs/build-log.txt

dkhostname=$containername

# PORT
#dkport=4000:4000

#xmount=/mnt/c/Users/jeang/Dropbox/w/o/pys/jgtpy:/work/jgtpy
#xmount=/a/www/_/app/o/pys/jgtpy:/work/jgtpy
xmount2=$HOME/.ssh:$HOME/.ssh


dkcommand=bash #command to execute (default is the one in the dockerfile)
#dkcommand="bash /work/build-n-release.sh"

dkextra=" -v /a:/a "

#dkextra=" -v $(pwd)/../../jgtapy-jgwill:/jgtapy -v $HOME/.pypirc:/root/.pypirc  -v $HOME/.pypirc:$HOME/.pypirc  -v $pysroot/..:/a/repos -v $srcroot:/src -v $binroot:/a/bin "

#dkmounthome=true


##########################
############# RUN MODE
#dkrunmode="bg" #default fg
#dkrestart="--restart" #default
#dkrestarttype="unless-stopped" #default


#########################################
################## VOLUMES
#dkvolume="myvolname220413:/app" #create or use existing one
#dkvolume="$containername:/app" #create with containername name



#dkecho=true #just echo the docker run


# Use TZ
#DK_TZ=1



#####################################
#Build related
#
##chg back to that user
#dkchguser=vscode

######################## HOOKS BASH
### IF THEY EXIST, THEY are Executed, you can change their names

dkbuildprebuildscript=dkbuildprebuildscript.sh
dkbuildbuildsuccessscript=dkbuildbuildsuccessscript.sh
dkbuildfailedscript=dkbuildfailedscript.sh
dkbuildpostbuildscript=dkbuildpostbuildscript.sh

###########################################

