#!/usr/bin/env bash

# Zip the setup.py, tests, requirements, README.md, and package
# Exclude caches, outputs, and complied files
# Output is in results

zip -r build-submission.zip \
	setup.py requirements.txt README.md results edges \
	-x *__pycache__* *out* *.pyc
