if [ -f /config/profile.txt ]; then
  cat /config/profile.txt
else
  echo "tune_profile=-1"
fi
