#!/bin/bash

ODIR=$( pwd ) # oh dear
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ "$#" -eq 3 ]; then
	cp $1 $DIR/src
	cp $2 $DIR/src
fi

cd $DIR/src

./corruptionpdfgen.py $1 $2 "${3}" && mv "${3}.pdf" $ODIR
if [ "$#" -eq 3 ]; then
	rm "${3}.aux" "${3}.log" "${3}.tex" "$1" "$2"
fi
cd ..
