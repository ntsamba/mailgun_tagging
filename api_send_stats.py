import requests
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

MAILGUN_DOMAIN = "YOUR_DOMAIN_NAME"  # e.g., sandbox123.mailgun.org
MAILGUN_API_KEY = "YOUR_API_KEY"

def fetch_tag_stats(days_back=1):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days_back)

    params = {
        "event": ["delivered", "opened", "clicked", "failed"],
        "start": format_datetime(start),
        "end": format_datetime(end),
        "resolution": "hour"
 }

    response = requests.get(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/stats/total",
        auth=("api", MAILGUN_API_KEY),
        params=params
 )

    if response.status_code == 200:
        return response.json()["stats"]
    else:
        print("Error:", response.status_code, response.text)
        return []

# Get All Stats
stats = fetch_tag_stats()
for day in stats:
    print(day["time"])
    for metric in ["delivered", "failed", "opened", "clicked"]:
        print(f"  {metric}: {day[metric]}")