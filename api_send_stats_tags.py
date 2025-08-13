import requests
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

MAILGUN_DOMAIN = "YOUR_DOMAIN_NAME"  # e.g., sandboxXXX.mailgun.org
MAILGUN_API_KEY = "YOUR_API_KEY"

def fetch_metrics(tag, hours_back):
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours_back)

    url = "https://api.mailgun.net/v1/analytics/metrics"

    payload = {
        "start": format_datetime(start),  # RFC 2822 format
        "end": format_datetime(end),
        "resolution": "hour",
        "duration": f"{hours_back}h",  # Not strictly required. Overwrites the start date
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
        url,
        auth=("api", MAILGUN_API_KEY),
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print("Metrics Filter by TAGs API response:")
        print(data)
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

fetch_metrics(tag="quote", hours_back=1)