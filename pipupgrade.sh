cat requirements.txt | while read PACKAGE; do pip install -U "$PACKAGE"; done
