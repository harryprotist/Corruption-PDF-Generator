#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

if [ "$#" -eq 3 ]; then
	cp $1 src
	cp $2 src
fi

cd src
./corruptionpdfgen.py $1 $2 "${3}" && mv "${3}.pdf" ..
if [ "$#" -eq 3 ]; then
	rm "${3}.aux" "${3}.log" "${3}.tex" "$1" "$2"
fi
cd ..
