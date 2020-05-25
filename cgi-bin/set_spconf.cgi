#!/bin/sh -e

ant_tmp=`cat /dev/stdin`

echo "$ant_tmp" > /config/spconf.txt

killall bmminer

echo "OK"
