#!/bin/bash

case "$1" in
  *.tar*) tar tf "$1";;
  *.zip) unzip -l "$1";;
  *.rar) unrar l "$1";;
  *.7z) 7z l "$1";;
  *.pdf) pdftotext "$1" -;;
  *.epub) ebook2text "$1";;
  *.doc) catdoc "$1" -;;
  *.docx) docx2txt "$1" -;;
  *.mkv) mediainfo "$1";;
  *.mp4) mediainfo "$1";;
  *) highlight -O ansi "$1" || cat "$1";;
esac
