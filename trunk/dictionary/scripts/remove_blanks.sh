#!/bin/bash

cat dictionary.xml | sed -e 's/^[ \t]*//' > tmp
cat tmp | sed ':a;N;$!ba;s/\n//g' > dictionary2.xml
rm tmp
mv dictionary2.xml dictionary.xml
