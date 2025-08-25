import smtplib
from email.message import EmailMessage
import sys 
import os
import json
import time
import random
import sqlite3


def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()  
    return text

if len(sys.argv) < 5:
    print("Usage: python controller.py <Server URL> <SMTP username> <SMTP Password> <limit>")
    sys.exit(1)

def read_emails_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Example: assumes a table called `leads` with a column `email`
    cursor.execute("SELECT email FROM emails WHERE status = ?", ("unused",))
    emails = [row[0] for row in cursor.fetchall()]

    conn.close()
    return emails

def update_lead_status(db_path, email, new_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Example: assumes a column `status` exists
    cursor.execute("""
        UPDATE emails
        SET status = ?
        WHERE email = ?
    """, (new_value, email))

    conn.commit()
    conn.close()

SMTP_SERVER = sys.argv[1]  
SMTP_PORT = 2525
SMTP_USERNAME = sys.argv[2]   
SMTP_PASSWORD = sys.argv[3]       


email_path = "emails"
rate_limit = sys.argv[4]

db_path = "./leads.db"
file_path_body = "emails/templates/body.txt"
file_path_subject = "emails/templates/subject.txt"  

body_words = read_words_from_file(file_path_body)
subject_words = read_words_from_file(file_path_subject)


count = 1
rate_limit = int(rate_limit)

emails = read_emails_from_db(db_path)

for email in emails:

    if count > rate_limit:
        break
    else:
        msg = EmailMessage()
        msg["From"] = SMTP_USERNAME
        msg["To"] = email.strip()
        msg["Subject"] = subject_words
        msg.set_content(body_words)

        try:
            # ⏱ Add random delay (e.g., 1 to 5 seconds)
            delay = random.uniform(10, 100)
            time.sleep(delay)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            print(f"✅ {count} - {email} - Delay:{delay} Seconds")
            count += 1
            update_lead_status(db_path, email, "used")

        except Exception as e:
            print(f"❌ {email} : {e}")