#!/bin/zsh
#
python3 python/prepare_data.py
python3 python/graphs.py
pdflatex ../slides/bank_twitter.tex
