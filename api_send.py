import requests

MAILGUN_DOMAIN = "YOUR_DOMAIN_NAME"
MAILGUN_API_KEY = "YOUR_API_KEY"


def send_tagged_email(to_email, is_html, subject, content, tracking_clicks, tracking_opens, tag):
    data={
            "from": f" <mailgun@{MAILGUN_DOMAIN}>",
            "to": to_email,
            "subject": subject,
            "o:tracking-clicks": tracking_clicks,
            "o:tracking-opens": tracking_opens,
            "o:tag": tag
 }
    if is_html:
        data["html"] = content
    else:
        data["text"] = content

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY), data=data
        
 )
    print("Status:", response.status_code)
    print("Response:", response.json())
    print()

# Email 1: Text based with tag welcome-email:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    is_html=False,
    subject="Welcome to our Email service!",
    content="Thanks for joining us. Email 1",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="welcome-email"
)

# Email 2: HTML based with tag welcome-email:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    is_html=True,
    subject="Welcome to our Email service!",
    content="""
    <html>
      <body>
        <h1>Welcome!</h1>
        <p>Email 2.  <p> 
        <p>Thanks for joining us.</p>
      </body>
    </html>
    """,
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="welcome-email"
)

## Email 3: Text based with tag newsletter:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    is_html=False,
    subject="August Newsletter!",
    content="Email 3. Attached is our August Newsletter.",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="newsletter"
)

# Email 4: HTML based with tag newsletter:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    is_html=True,
    subject="HTML Newsletter",
    content="""
    <html>
      <body>
        <h1>August Newsletter!</h1>
        <p>Email 4.  </p>
        <p>Attached is our August Newsletter.</p>
      </body>
    </html>
    """,
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)

# Email 5: Text based with tag quote:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    is_html=False,
    subject="Quote for Email service!",
    content="Email 5. There are four tiers for pricing. More details can be found here: https://www.mailgun.com/pricing/.",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)

# Email 6: HTML based with tag quote:
send_tagged_email(
    to_email="YOUR_RECIPIENT_EMAIL",
    is_html=True,
    subject="HTML Newsletter",
    content="""
    <html>
      <body>
        <h1>Quote for Email service!</h1>
        <p>Email 6.  </p>
        <p>Here are four tiers for pricing. More details can be found here: https://www.mailgun.com/pricing/. </p>
      </body>
    </html>
    """,
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)

# Email 7: Text based with tag quote:
send_tagged_email(
    to_email="mailgun123456demo@gmail.com", # doesn't exist
    is_html=False,
    subject="Quote for Email Service",
    content="There are four tiers for pricing. More details can be found here. Email 7",
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)

# Email 8: HTML based with quote tag:
send_tagged_email(
    to_email="mailgun123456demo@gmail.com", # doesn't exist
    is_html=False,
    subject="Quote for Email Service",
    content="""
    <html>
      <body>
        <h1>Quote for Email service!</h1>
        <p>here are four tiers for pricing. More details can be found here: https://www.mailgun.com/pricing/. Email 8</p>
      </body>
    </html>
    """,
    tracking_clicks="yes",
    tracking_opens="yes",
    tag="quote"
)