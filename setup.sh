#!/bin/bash

function install_python_packages {
	pip install -r requirements.txt
}

function install_spacy_cnn {
	python3 -m spacy download en_core_web_sm
	python3 -m spacy download en_core_web_md
}

install_python_packages
install_spacy_cnn
