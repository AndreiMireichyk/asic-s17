#!/bin/sh -e

ant_tmp=`cat /dev/stdin`

case $ant_tmp in
    ''|*[!0-9]*) echo "wrong format" ;;
    *) cp /config/profiles/$ant_tmp/* /config; killall bmminer ;;
esac

echo "1"

