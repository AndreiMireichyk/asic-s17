#!/bin/sh -e

ant_tmp=`cat /dev/stdin`

echo "$ant_tmp" > /config/manual_freqs.txt

sync &

killall bmminer

echo "OK"
