#!/bin/sh
#set -x

if [ -f /config/stop-mining ]; then
  cat /config/stop-mining
else
  echo "ok"
fi