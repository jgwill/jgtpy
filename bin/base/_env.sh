ctlid=2408011203
export dockertag=jgwill/jgt:jgtpy
dockertag1=jgwill/jgt:cds

containername=cds
dkhostname=$containername

# PORT
#dkport=4000:4000

if [ -f "/etc/jgt/config.json" ];then
        xmount=/etc/jgt/config.json:/etc/jgt/config.json

fi
xmount2=/tmp/fxdata:/data
rm -rf /tmp/fxdata
mkdir -p /tmp/fxdata
#xmount2=$HOME/.jgt/settings.json:$HOME/.jgt/settings.json
#xmount2=/var:/a/var


dkcommand=bash #command to execute (default is the one in the dockerfile)

dkextra=" -v $(realpath $(pwd)/../../):/app \
        -v /home/jgi/.jgt:/home/jgi/.jgt "
    #    -e JGT_CONFIG=$JGT_CONFIG "

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
# Unset deprecated
unset DOCKER_BUILDKIT

