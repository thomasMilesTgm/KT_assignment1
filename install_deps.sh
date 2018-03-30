#!/bin/bash
# Installs all the libraries required to run this application

# dependencies: python-pip
#               python 2.4 or higher
#               git

pip install python-Levenshtein
pip install fuzzywuzzy
git clone https://github.com/ryszard/python-ngrams.git $(pwd)/src/
