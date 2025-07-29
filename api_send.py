import requests

MAILGUN_DOMAIN = "YOUR_DOMAIN_NAME"  # e.g. sandboxXXX.mailgun.org
MAILGUN_API_KEY = "YOUR_API_KEY"

def send_tagged_email(to_email, subject, text, tracking_clicks, tracking_opens, tag):
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f" <mailgun@{MAILGUN_DOMAIN}>",
            "to": to_email,
            "subject": subject,
            "text": text,
            "o-tracking-clicks": tracking_clicks,
            "o-tracking-opens": tracking_opens,
            "o:tag": tag
 }
 )
    print("Status:", response.status_code)
    print("Response:", response.json())

# Email 1 with tag welcome-tag:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    subject="Welcome to our Email service!",
    text="Thanks for joining us. Email 1",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="welcome-email"
)

# Email 2 with tag newsletter:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    subject="July Newsletter!",
    text="Attached is our July Newsletter. Email 2",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="newsletter"
)

# Email 3 with quote tag:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    subject="Quote for Email service!",
    text="There are four tiers for pricing. More details can be found here: https://www.mailgun.com/pricing/. Email 3",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)

# Email 4 with quote tag:
send_tagged_email(
    to_email="mailgun12345demo@gmail.com", # doesn't exist
    subject="Quote for Email Service",
    text="There are four tiers for pricing. More details can be found here. Email 4",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)