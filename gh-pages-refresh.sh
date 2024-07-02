make docs && (cp -r docs/_build/html/* ../gh-pages-jgtpy/ && cd ../gh-pages-jgtpy/ && (git add .;git commit . -m update:doc;git push))

