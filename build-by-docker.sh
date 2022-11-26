. _env.sh
if [ "$HOSTNAME" != "$dkhostname" ]; then
	echo "Launching DockerTAG: $dockertag to build and publish "

	dkrun "bash /work/build-n-release.sh"
else
	echo "--------------"
	. build-n-release.sh
fi

