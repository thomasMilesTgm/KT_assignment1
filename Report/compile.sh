#!/bin/bash

pdflatex Report.tex
bibtex Report
pdflatex Report.tex
pdflatex Report.tex

