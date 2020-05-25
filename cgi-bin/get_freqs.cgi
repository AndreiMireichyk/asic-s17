if [ -f /config/freqs.txt ]; then
  cat /config/freqs.txt
else
  echo "none"
fi
