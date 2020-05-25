#!/bin/sh
#set -x

tz=`cat /dev/stdin | sed 's/tz=//' | sed 's/%2B/+/'`

echo "$tz" | grep -E "^[GMT+-\d]+\$" > /dev/null

# ensure that cron expr contains only valid string
if [ $? -ne 0 ]; then
  echo "ok"
  exit 0
fi


path=/usr/share/zoneinfo/Etc/${tz}
cp $path /config/localtime

ln -s /config/localtime /etc/localtime
/etc/init.d/ntpdate.sh

sleep 2s

sync &

echo "ok"

