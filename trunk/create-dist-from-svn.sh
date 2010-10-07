#!/bin/sh

mkdir ../promogest-dist
cp -rp *  ../promogest-dist
cd ../promogest-dist
find ./ -name .svn* -exec rm -rf \{\} \;
find ./ -name *.pyc -exec rm -rf \{\} \;
chmod +x core/promogest.py
