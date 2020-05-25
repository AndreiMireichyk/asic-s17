#!/bin/sh

if [ -f /config/fan.conf ]; then
  echo "1"
else
  echo "0"
fi
