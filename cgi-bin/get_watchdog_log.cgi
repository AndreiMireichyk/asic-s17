if [ -f /config/watchdog.log ]; then
  cat /config/watchdog.log
else
  echo "."
fi
