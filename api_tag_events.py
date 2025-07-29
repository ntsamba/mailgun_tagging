import requests
import csv
from collections import defaultdict
from datetime import datetime, timedelta, timezone


MAILGUN_DOMAIN = "YOUR_DOMAIN_NAME"
MAILGUN_API_KEY = "YOUR_API_KEY"

TAGS = ["TAG_1", "TAG_2", "TAG_3"] #["newsletter", "welcome-email", "quote"]
EVENTS = ["delivered", "opened", "clicked", "failed"]

BASE_URL = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/events"

# Set 1-hour range
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(hours=2)
begin_epoch = int(start_time.timestamp())
end_epoch = int(end_time.timestamp())

def fetch_events(tag, event_type, begin, end):
    params = {
        "tags": tag,
        "event": event_type,
        "begin": str(begin),
        "end": str(end),
        "limit": 300  # max is 300
    }
    response = requests.get(BASE_URL, auth=("api", MAILGUN_API_KEY), params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error for tag '{tag}' and event '{event_type}': {response.status_code} - {response.text}")
        return []

# Data structure to hold output
csv_rows = []

for tag in TAGS:
    print(f"\nTag: {tag}")

    # Dictionary to group counts by hour and event type
    hourly_summary = defaultdict(lambda: defaultdict(int))

    for event_type in EVENTS:
        items = fetch_events(tag, event_type, begin_epoch, end_epoch)

        for item in items:
            ts = item.get("timestamp")
            if ts:
                dt = datetime.fromtimestamp(ts)
                hour_key = dt.strftime("%Y-%m-%d %H:00")
                hourly_summary[hour_key][event_type] += 1

    # Print and collect rows
    for hour in sorted(hourly_summary.keys()):
        counts = hourly_summary[hour]
        delivered = counts.get("delivered", 0)
        opened = counts.get("opened", 0)
        clicked = counts.get("clicked", 0)
        failed = counts.get("failed", 0)

        print(f"\nHour: {hour}")
        print(f"  Delivered : {delivered}")
        print(f"  Opened    : {opened}")
        print(f"  Clicked   : {clicked}")
        print(f"  Failed    : {failed}")

        csv_rows.append({
            "tag": tag,
            "hour": hour,
            "delivered": delivered,
            "opened": opened,
            "clicked": clicked,
            "failed": failed,
        })

# Export to CSV
csv_filename = f"mailgun_events_{start_time.strftime('%Y%m%d_%H%M')}_to_{end_time.strftime('%H%M')}.csv"

with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["tag", "hour", "delivered", "opened", "clicked", "failed"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"\nResults exported to {csv_filename}")