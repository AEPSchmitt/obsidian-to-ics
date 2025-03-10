import os
import re
from datetime import datetime
from ics import Calendar, Event
from ftplib import FTP_TLS
import pytz

# Timezone settings
TIMEZONE = "Europe/Copenhagen"
tz = pytz.timezone(TIMEZONE)

# Path to your Obsidian daily notes folder
DAILY_NOTES_FOLDER = "/path/to/your/obsidian/daily notes/"
OUTPUT_ICS_FILE = "obsidian.ics"

# FTP Credentials
FTP_HOST = "yourserver.com"
FTP_USER = "username"
FTP_PASS = "password"
FTP_REMOTE_PATH = "/public_html/calendar/obsidian.ics"  # Where to store the file

# Regular expression for extracting event timestamps
# Each event should be a line like: "- [ ] hh:mm - eventname"
EVENT_REGEX = re.compile(r"- \[ \] (\d{2}:\d{2})\s*-\s*(.+)")

def parse_events_from_md(file_path, event_date):
    """Parses events from a Markdown file, extracting times and descriptions."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.readlines()

    events = []
    for line in content:
        print(line)
        match = EVENT_REGEX.match(line.strip())
        if match:
            time_str, event_name = match.groups()
            event_time = datetime.strptime(time_str, "%H:%M").time()
            events.append((event_time, event_name, event_date))

    return events

def extract_date_from_filename(filename):
    """Extracts the date from the filename formatted as DD-MM-YYYY.md"""
    try:
        return datetime.strptime(filename[:-3], "%d-%m-%Y").date()
    except ValueError:
        return None  # Skip files that don’t match the expected format

def create_ics_file(events):
    """Creates an .ics file containing all events with timezone support."""
    cal = Calendar()
    
    for event_time, event_name, event_date in events:
        event = Event()
        event.name = event_name
        
        # Combine date and time then localize it
        dt = datetime.combine(event_date, event_time)
        dt = tz.localize(dt)  # Convert to timezone-aware datetime
        
        event.begin = dt
        cal.events.add(event)
    
    with open(OUTPUT_ICS_FILE, "w") as f:
        f.writelines(cal)
    
    print(f"ICS file '{OUTPUT_ICS_FILE}' created with {len(events)} events.")

def upload_to_ftp(file_path):
    """Uploads the given file to an FTPS server."""
    try:
        ftps = FTP_TLS(FTP_HOST)
        ftps.login(FTP_USER, FTP_PASS)
        ftps.prot_p()  # Enable secure data connection
        
        with open(file_path, "rb") as f:
            ftps.storbinary(f"STOR {FTP_REMOTE_PATH}", f)

        ftps.quit()
        print(f"Successfully uploaded '{file_path}' to '{FTP_REMOTE_PATH}' on {FTP_HOST}.")
    except Exception as e:
        print(f"FTP Upload Error: {e}")

def main():
    """Main function to process all daily notes and generate an ICS file."""
    all_events = []

    for filename in os.listdir(DAILY_NOTES_FOLDER):
        if filename.endswith(".md"):
            event_date = extract_date_from_filename(filename)
            if event_date:
                file_path = os.path.join(DAILY_NOTES_FOLDER, filename)
                events = parse_events_from_md(file_path, event_date)
                all_events.extend(events)

    if all_events:
        create_ics_file(all_events)
        upload_to_ftp(OUTPUT_ICS_FILE)
    else:
        print("No events found in the daily notes.")

if __name__ == "__main__":
    main()
