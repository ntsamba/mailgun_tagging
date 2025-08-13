import requests
import csv
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

# Mailgun credentials
MAILGUN_DOMAIN = "YOUR_DOMAIN_NAME"  # e.g., sandboxXXX.mailgun.org
MAILGUN_API_KEY = "YOUR_API_KEY"

# Tags to fetch
TAGS = ["TAG_1", "TAG_2", "TAG_3"] #["newsletter", "welcome-email", "quote"]

# Time range in hours
HOURS_BACK = 1

# API endpoint
METRICS_URL = "https://api.mailgun.net/v1/analytics/metrics"

def fetch_metrics(tag, hours_back):
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours_back)

    payload = {
        "start": format_datetime(start),  # RFC 2822 format
        "end": format_datetime(end),
        "resolution": "hour",
        "duration": f"{hours_back}h",
        "dimensions": ["time"],
        "metrics": [
            "accepted_count",
            "delivered_count",
            "clicked_rate",
            "opened_rate",
            "failed_count"
        ],
        "filter": {
            "AND": [
                {
                    "attribute": "tag",
                    "comparator": "=",
                    "values": [
                        {
                            "label": tag,
                            "value": tag
                        }
                    ]
                }
            ]
        },
        "include_subaccounts": True,
        "include_aggregates": True
    }

    response = requests.post(
        METRICS_URL,
        auth=("api", MAILGUN_API_KEY),
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching metrics for tag '{tag}': {response.status_code} - {response.text}")
        return None

# Collect CSV rows
csv_rows = []

for tag in TAGS:
    print(f"\nMetrics for tag: {tag}")
    print("=" * 50)

    data = fetch_metrics(tag, HOURS_BACK)
    if not data or "items" not in data:
        print("No data returned.\n")
        continue
    
    #print(data["items"])
    #print()
    #print("#######")
    for item in data["items"]:
        # Extract timestamp
        time_dim = item["dimensions"][0]["value"]
        metrics = item["metrics"]
        accepted_count = metrics.get("accepted_count", 0)
        delivered_count = metrics.get("delivered_count", 0)
        failed_count = metrics.get("failed_count", 0)
        opened_rate = metrics.get("opened_rate")
        clicked_rate = metrics.get("clicked_rate", "0.0000")

        # Pretty console output
        print(f"{time_dim}")
        print(f"  Accepted : {accepted_count}")
        print(f"  Delivered: {delivered_count}")
        print(f"  Failed   : {failed_count}")
        print(f"  Opened % : {opened_rate}")
        print(f"  Clicked %: {clicked_rate}")
        print("-" * 50)

        # Append row for CSV
        csv_rows.append({
            "tag": tag,
            "time": time_dim,
            "accepted_count": accepted_count,
            "delivered_count": delivered_count,
            "failed_count": failed_count,
            "opened_rate": opened_rate,
            "clicked_rate": clicked_rate
        })

# Export to CSV
start_time = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)
end_time = datetime.now(timezone.utc)
csv_filename = f"mailgun_metrics_{start_time.strftime('%Y%m%d_%H%M')}_to_{end_time.strftime('%H%M')}.csv"

with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["tag", "time", "accepted_count", "delivered_count", "failed_count", "opened_rate", "clicked_rate"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"\nResults exported to {csv_filename}")
