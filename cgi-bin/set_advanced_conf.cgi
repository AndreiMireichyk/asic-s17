#!/bin/sh -e

ant_tmp=`cat /dev/stdin`

echo "$ant_tmp" > /config/config.conf

# killall bmminer

echo "OK"
