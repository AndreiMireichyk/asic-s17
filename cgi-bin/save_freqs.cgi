#!/bin/sh -e

ant_tmp=`cat /dev/stdin`

echo "$ant_tmp" > /tmp/save_freq.txt

while [ -f /tmp/save_freq.txt ]
do
  sleep 1
done

echo "OK"
