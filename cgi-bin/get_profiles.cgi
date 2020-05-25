#!/bin/sh -e

ls /config/profiles -F | grep \/$ | sed 's/\///'

echo "."