#!/usr/bin/env bash

# Zip the setup.py, tests, requirements, README.md, and package
# Exclude caches, outputs, and complied files
# Output is in results
DIR=$(pwd)

if [ $1 ]; then
FILENAME="CAWLEY-EDWARDS_Austin_${1}.zip"
else
FILENAME="CAWLEY-EDWARDS_Austin.zip"
fi

# Readme documentation
pandoc -s -o README.pdf README.md WRITEUP-2.md

doxygen doxygen.config
cd docs/latex
make
mv refman.pdf ${DIR}

cd ${DIR}
zip -r ${FILENAME} \
	setup.py requirements.txt README.md results edges \
	-x *__pycache__* *out* *.pyc

