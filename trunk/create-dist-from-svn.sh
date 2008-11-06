#!/bin/sh

mkdir ../promogest-dist
cp -rp *  ../promogest-dist
cd ../promogest-dist
find ./ -name .svn* -exec rm -rf \{\} \;
find ./ -name *.pyc -exec rm -rf \{\} \;
cd data/reg/tab
rm -f *.sql
cd ../view
rm -f *.sql
cd ../../../
rm create-dist-from-svn.sh
rm -f python/configure_full.dist
chmod +x python/promogest.py
