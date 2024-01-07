export QT_QPA_PLATFORM=xcb
if [ -e ".env" ]; then
  source .env
fi

# Optimally we would run it in the shell
python pto-pers-panel-03.py &> /dev/null && \
  (cd $LDIR;scp pto-full.html $SSH_TDIR/pto-full.html && echo "You can probably view it at : $JGT_HTTP_PUB_SVR_ADDR_BASE/pto-full.html")||\
  echo "Failed to run pto-pers-panel-03.py"  

# Tries to add and commit them
(cd $LDIR && pwd && git add *html && git commit . -m "Updated charts" ; git push) || echo "Failed to add and commit charts"
