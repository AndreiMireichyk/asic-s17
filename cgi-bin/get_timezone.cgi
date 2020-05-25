#!/bin/sh
#set -x

if [ -e /config/localtime ];then
  cat /config/localtime | sed -rn 's/.*[>T]([-+0-9]+)$/GMT+\1/p' | sed 's/+-/-/' | sed 's/+0/0/'
else
  echo ""
fi
