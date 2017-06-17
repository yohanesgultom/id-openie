#!/bin/sh

echo "converting to html"
pandoc -f latex -t html -o thesis.html --bibliography ../pustaka.bib thesis.tex

