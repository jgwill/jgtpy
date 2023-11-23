

(cd _snote_content_cache;for h in $(ls *html);do \
	ff=${h%.*};html2text $h > $ff.conv.txt;done; cat *.conv.txt > ../data/snote_aggregated.md )

