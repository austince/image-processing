#!/usr/bin/env bash


if [ $1 == 'help' ]; then
	echo "Usage: build-submission.sh [ZIP_EXT] [WRITEUP-FILE]"
	exit 0
fi

DIR=$(pwd)
PKG_NAME=image_processing
FILENAME="CAWLEY-EDWARDS_Austin_${1}.zip"
WRITEUP_FILE=${2}

# Readme documentation
#pandoc -s -o README.pdf README.md ${WRITEUP_FILE}
pandoc -s -o README.pdf -t html5 --css readme.css README.md ${WRITEUP_FILE}

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

