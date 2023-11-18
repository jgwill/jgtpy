
for p in $(cat _install-pandas-fix.txt | tr "<" " "| tr ">" " "|awk '/req/ {print $4}'); do
	echo "pip install $p" >> _pip-install-pandas-fix.sh
done

