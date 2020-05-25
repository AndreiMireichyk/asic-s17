#!/bin/sh
#set -x

rm /config/stop-mining
killall bmminer

sync &

echo "ok"
