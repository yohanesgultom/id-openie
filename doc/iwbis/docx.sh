#!/bin/bash

echo "converting to docx.."
pandoc -f latex -t docx -o iwbis.docx --bibliography ../pustaka.bib iwbis.tex

