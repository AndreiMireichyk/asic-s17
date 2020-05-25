#!/bin/sh

rm -f /config/fan.conf

if grep -q tune_profile=1[0-9] "/config/profile.txt"; then
  rm /config/profile.txt
fi

echo "ok"
