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
def reverse_word(word: str) -> str:
    """Reverses the characters in a word."""
    return word[::-1]

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
    """Reads the last N emails from the inbox, including the body content."""
    sender = os.getenv("SENDER_EMAIL")
    pw = os.getenv("EMAIL_APP_PASSWORD")
    
    try:
        # Connect and login
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender, pw)
        mail.select("inbox")
        
        # Search for all emails and get the last 'count' IDs
        _, messages = mail.search(None, "ALL")
        all_ids = messages[0].split()
        ids = all_ids[-count:]
        
        results = []
        # Process from newest to oldest
        for e_id in reversed(ids):
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the raw bytes into an email object
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    from_address = msg["from"]
                    
                    # Extract the body
                    body = ""
                    if msg.is_multipart():
                        # Iterate through email parts (text, html, attachments)
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            # We specifically want the plain text body
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                payload = part.get_payload(decode=True)
                                body = payload.decode(errors="replace")
                                break 
                    else:
                        # Not multipart, just extract the payload directly
                        payload = msg.get_payload(decode=True)
                        body = payload.decode(errors="replace")

                    # Format the output for the LLM
                    entry = f"FROM: {from_address}\nSUBJECT: {subject}\nBODY:\n{body.strip()}\n"
                    results.append(entry)
        
        mail.logout()
        return "\n" + ("="*30) + "\n".join(results) if results else "No emails found."

    except Exception as e:
        return f"Error reading inbox: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")