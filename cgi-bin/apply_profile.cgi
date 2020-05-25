#!/bin/sh -e

ant_tmp=`cat /dev/stdin`

echo "$ant_tmp" > /config/profile.txt

#/etc/init.d/cgminer.sh restart &

sync &

killall bmminer

echo "OK"
