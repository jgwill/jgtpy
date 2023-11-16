for f in *py;do sed -i 's/from forexconnect\./from ./g' $f;done
for f in *py;do sed -i 's/from forexconnect/from ./g' $f;done

