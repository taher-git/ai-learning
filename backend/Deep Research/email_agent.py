import os
from typing import Dict
from agents import Agent, function_tool
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


load_dotenv(override=True)
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given body to all sales prospects via Resend """
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    # Set up email sender, recipient, and content
    from_email = "from_email@gmail.com"  # Replace with your verified sender
    to_email = "to_email@gmail.com"  # Replace with recipient's email
    
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(from_email, GMAIL_APP_PASSWORD)
        s.send_message(msg)
    print('Sent')
    return "success"

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
