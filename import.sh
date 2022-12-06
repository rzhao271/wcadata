#!/bin/sh

mariadb -u "$USER" -p wcadata < WCA_export.sql > output.log 2>&1

if [ -s output.log ]
then
    echo 'Import failed'
    exit 1
fi

echo 'Import succeeded'
