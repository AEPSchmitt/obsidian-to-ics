# Obsidian to .ics
Parses Obsidian daily notes into .ics file and uploads it via FTP.

Quick and dirty python script to synchronize Obsidian Daily Notes with any calendar service.

The following configurations will need to be set, in order for the script to work:

```

DAILY_NOTES_FOLDER = "/path/to/your/obsidian/daily notes/"

FTP_HOST = "yourserver.com"
FTP_USER = "username"
FTP_PASS = "password"
FTP_REMOTE_PATH = "/public_html/calendar/obsidian.ics"  # Where to store the file

UPLOAD_ICS = True
```

Set `UPLOAD_ICS` to `False` to skip FTP upload.
