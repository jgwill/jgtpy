

(cd ../jgtml && . upjgtpy_version.sh)

(conda activate jgtsd&>/dev/null && pip install -U jgtpy&>/dev/null && echo "jgtsd environment updated" || echo "jgtsd environment not found or pip install failed")

