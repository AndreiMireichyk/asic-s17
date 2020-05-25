#!/bin/sh
#set -x

if [ -e /config/stats ]; then
    for f in /tmp/stats/*
    do
	echo -n $(basename $f) && echo -n " " && cat $f | tr '\n' ' ' && echo ""
    done
else
    echo ""
fi
