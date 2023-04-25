#!/bin/bash

install pdftotext: https://pypi.org/project/pdftotext/

sudo apt install build-essential
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/marko/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

brew install tesseract
pip install -U sentence-transformers
pip install chromadb
python -m spacy download en_core_web_lg to get "en_core_web_lg"
pip install requierments.txt
