#!/bin/bash

#laczy pliki w formacie TEI w jeden plik
#nastepnie parsuje ten plik do formatu c5
#i z formatu c5 do formatu DICT

cd scripts

#polaczenie plikow TEI w jeden plik TEI dictionary.xml
./concatenate.sh

#usuniecie spacji i tabulacji pomiedzy wezlami xml'a (zeby python nie czytal pustych wezlow) w pliku dictionary.xml
./remove_blanks.sh

#usuniecie wczesniejszej listy slowek
rm -f list

#usuniecie wczesniejszego pliku dictionary.c5
rm -f dictionary.c5

#przekopiowanie naglowka do pliku dictionary.c5
cat header > dictionary.c5

#przeniesienie dictionary.c5 do katalogu c5
mv dictionary.c5 ../c5/

#parsowanie dictionary.xml do dictionary.c5
python parse.py

#usuniecie niepotrzebnego juz pliku dictionary.xml
rm dictionary.xml

cd ../c5

#utworzenie slownika w formacie DICT
dictfmt -t --utf8 eng-pol  < dictionary.c5 2>/dev/null

#przekopiowanie slownika do katalogu DICT
dictzip -k eng-pol.dict
mv eng-pol.dict.dz ../DICT
mv eng-pol.dict ../DICT
mv eng-pol.index ../DICT
