#!/bin/bash
#laczy pliki TEI w jeden plik TEI
cd ..
cd TEI
rm -f dictionary.xml

head -n 8 a.xml > dictionary.xml


for i in `ls *.xml | grep -v dictionary.xml`
do
    head -n -1 $i > $i.tmp
    tail -n +9 $i.tmp >> dictionary.xml
    rm $i.tmp
done

tail -n 1 a.xml >> dictionary.xml


mv dictionary.xml ../scripts
