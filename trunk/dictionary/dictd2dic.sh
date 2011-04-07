#!/bin/bash
# dictd2dic conversion script
# Original adapted to Ubuntu 10.04 LTS and usage with the 
# dict-freedict-X-Y packages (apt-cache search dict-freedict)
#
# Usage: sudo dictd2dic.sh freedict-eng-deu
#
TMPDIR=/tmp/$(basename $0)
DICTPREFIX="dictd_www.dict.org_"
DDIR=/usr/share/dictd
TDIR=/usr/share/stardict/dic
D2D=/usr/lib/stardict-tools/dictd2dic

if [ -e $TMPDIR ]; then
    rm -R $TMPDIR
fi
mkdir $TMPDIR
cd $TMPDIR

#getting the dictionaries
cp $DDIR/$1.{dict.dz,index} .

# decompressing the .dict.dz into a .dict file
if test -e $1.dict.dz; then dictunzip $1.dict.dz; fi
if test -e $1.dict; then
    echo "Please wait..."
    touch $1.idxhead
    echo "StarDict's dict ifo file" >$DICTPREFIX$1.ifo
    echo version=2.4.2 >>$DICTPREFIX$1.ifo

    echo wordcount=`$D2D $1 |grep 'wordcount:' |cut -b 12-` >>$DICTPREFIX$1.ifo

    echo idxfilesize=`stat -c %s $DICTPREFIX$1.idx` >>$DICTPREFIX$1.ifo
    echo bookname=$1 >>$DICTPREFIX$1.ifo
    echo date=2007.01.01 >>$DICTPREFIX$1.ifo
    echo sametypesequence=m >>$DICTPREFIX$1.ifo
    rm $1.idxhead
    echo -e "\e[32mSucessfully created $DICTPREFIX$1.\e[0m"
    echo "Installing the converted dictionary (sudo)..."
    if sudo cp $DICTPREFIX$1* $TDIR; then
	echo "The dictionary was installed $TDIR"
        # cleanup
	cd /tmp
	rm -rf $TMPDIR
	echo "Restart StarDict now!"
    else
	echo -e "\e[31mUnable to install dictionary to $TDIR\e[0m"
	echo "The converted dictionary is availably in $TMPDIR"
	echo "Remove $TMPDIR manually before converting another dictionary"
	echo "(rm -rf $TMPDIR)."
    fi
else
    echo "Usage: dictd2dic.sh freedict-eng-deu"
fi
