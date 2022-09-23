#!/bin/sh

# prepare the zips
mkdir zips
rm "zips/submission.zip"

INCLUDED="src test .gitignore LICENSE README.md"

EXCLUDED="src/__pycache__/ src/__pycache__/** test/__pycache__/ test/__pycache__/**"

zip -r "zips/submission.zip" $INCLUDED -x $EXCLUDED