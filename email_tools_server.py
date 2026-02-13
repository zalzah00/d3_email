# email_tools_server.py
import os
import smtplib
import imaplib
import email
from email.message import EmailMessage
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("EmailTools")

@mcp.tool()
def send_email(recipient: str, subject: str, body: str) -> str:
    """Sends an email with a custom subject and body."""
    sender = os.getenv("SENDER_EMAIL")
    pw = os.getenv("EMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, pw)
            server.send_message(msg)
        return f"Successfully sent to {recipient}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def read_inbox(count: int = 5) -> str:
    """Reads the last N emails from the inbox."""
    sender = os.getenv("SENDER_EMAIL")
    pw = os.getenv("EMAIL_APP_PASSWORD")
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender, pw)
        mail.select("inbox")
        _, messages = mail.search(None, "ALL")
        ids = messages[0].split()[-count:]
        
        results = []
        for e_id in reversed(ids):
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    results.append(f"From: {msg['from']} | Sub: {msg['subject']}")
        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")