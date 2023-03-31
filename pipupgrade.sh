cat requirements.txt | while read PACKAGE; do pip install -U "$PACKAGE"; done
python3 -m  pipreqs.pipreqs --force
