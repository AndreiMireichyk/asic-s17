if [ -f /config/manual_freqs.txt ]; then
  cat /config/manual_freqs.txt
else
  echo "none"
fi
