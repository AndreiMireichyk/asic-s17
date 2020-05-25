#!/bin/sh -e

cat /config/profile.txt | sed 's/tune_status=1/tune_status=2/g' > /config/profile_bak
rm /config/profile.txt
mv /config/profile_bak /config/profile.txt

killall bmminer

echo "Tune stopped" >> /tmp/tune_log.txt

echo "ok"
