#!/bin/bash

INPUT=books_data.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read id title pdf_url
do
	echo "id : $id"
	echo "title : $title"
	echo "pdf_url : $pdf_url"

    wget -c $pdf_url -O "كتب مؤسسة هنداوي/$title.pdf"
done < $INPUT
IFS=$OLDIFS
