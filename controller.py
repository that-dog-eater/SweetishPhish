import smtplib
from email.message import EmailMessage
import sys 
import os
import json
import time
import random


def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()  
    return text

if len(sys.argv) < 5:
    print("Usage: python controller.py <Server URL> <SMTP username> <SMTP Password> <date> <limit>")
    sys.exit(1)


SMTP_SERVER = sys.argv[1]  
SMTP_PORT = 2525
SMTP_USERNAME = sys.argv[2]   
SMTP_PASSWORD = sys.argv[3]       

json_leads_path = "json_leads"
email_path = "emails"
file_name = sys.argv[4]
file = os.path.join(email_path, file_name + ".json")
rate_limit = sys.argv[5]


file_path_body = "emails/templates/body.txt"
file_path_subject = "emails/templates/subject.txt"  

body_words = read_words_from_file(file_path_body)
subject_words = read_words_from_file(file_path_subject)

with open(file, 'r') as f: 
    data = json.load(f)

count = 1
rate_limit = int(rate_limit)

for email in data['emails']:

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
            delay = random.uniform(300, 600)
            time.sleep(delay)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            print(f"✅ {count} - {email} - Delay:{delay} Seconds")
            count += 1
        except Exception as e:
            print(f"❌ {email} : {e}")