#!/usr/bin/env bash

DIR=$(pwd)
PKG_NAME=detection

if [ $1 ]; then
FILENAME="CAWLEY-EDWARDS_Austin_${1}.zip"
else
FILENAME="CAWLEY-EDWARDS_Austin.zip"
fi

# Readme documentation
#pandoc -s -o README.pdf README.md WRITEUP-2.md
pandoc -s -o README.pdf -t html5 --css readme.css README.md WRITEUP-2.md

doxygen doxygen.config
cd docs/latex
make
mv refman.pdf ${DIR}

cd ${DIR}

# Zip the setup.py, tests, requirements, compiled pdfs, and package
# Exclude caches, temp outputs, markdown, and complied python files
# Output is in results
zip -r ${FILENAME} \
	setup.py requirements.txt README.md results *.pdf ${PKG_NAME} \
	-x *__pycache__* *out* *.pyc *.md

