import pandas as pd

df = pd.read_csv("AI Agent Demo/email_classifier/data/emails.csv", nrows=200000)

def label_email(text):
    text = str(text).lower()
    billing_keywords = [
        "invoice", "payment", "bill", "subscription", "charge", "refund", "price", "cost", "fee", "receipt"
    ]
    spam_keywords = [
        "spam", "junk", "scam", "phishing", "malware", "virus", "ad", "promotion", "unsubscribe", "lottery"
    ]
    technical_keywords = [
        "password", "login", "error", "issue", "bug", "support", "crash", "network", "update", "install"
    ]
    personal_keywords = [
        "lunch", "party", "family", "dinner", "movie", "friend", "meet", "coffee", "trip", "vacation"
    ]
    work_keywords = [
        "meeting", "project", "deadline", "report", "presentation", "client", "team", "schedule", "appointment", "contract"
    ]
    promotional_keywords = [
        "sale", "offer", "discount", "promotion", "deal", "newsletter", "event", "webinar", "contest", "giveaway"
    ]
    social_keywords = [
        "friend", "family", "social", "network", "community", "group", "chat", "message", "post", "comment"
    ]

    if any(keyword in text for keyword in billing_keywords):
        return "Billing"
    elif any(keyword in text for keyword in spam_keywords):
        return "Spam"
    elif any(keyword in text for keyword in technical_keywords):
        return "Technical"
    elif any(keyword in text for keyword in personal_keywords):
        return "Personal"
    elif any(keyword in text for keyword in work_keywords):
        return "Work"
    elif any(keyword in text for keyword in promotional_keywords):
        return "Promotional"
    elif any(keyword in text for keyword in social_keywords):
        return "Social"
    else:
        return "Other"

df['label'] = df['message'].apply(label_email)

# fileter out rows where label is Other
# df = df[df['label'] != 'Other']
df.to_csv("AI Agent Demo/email_classifier/data/emails_labeled.csv", index=False)
print(df.head())