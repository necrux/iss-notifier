# iss-notifier
Get information about the ISS, and its current location. You can also configure the app for nightly emails when the ISS is overhead.
```
  _____  _____ _____ 
 |_   _|/ ____/ ____|
   | | | (___| (___  
   | |  \___ \\___  \ 
  _| |_ ____) |___) |
 |_____|_____/_____/ 
```

## Configure for Email
```main.py --configure```

## Configure Email Notifications
```
./main.py -t '<LAT>' -g '<LONG>' -n
```

For best results, configure this as a cron job that runs every minute.