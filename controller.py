import smtplib
from email.message import EmailMessage
import sys 
import os
import json

def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()  
    return text

if len(sys.argv) < 5:
    print("Usage: python controller.py <Server URL> <SMTP username> <SMTP Password> <date>")
    sys.exit(1)


SMTP_SERVER = sys.argv[1]  
SMTP_PORT = 2525
SMTP_USERNAME = sys.argv[2]   
SMTP_PASSWORD = sys.argv[3]       

json_leads_path = "json_leads"
email_path = "emails"
file_name = sys.argv[4]
file = os.path.join(email_path, file_name + ".json")

file_path_body = "emails/templates/body.txt"
file_path_subject = "emails/templates/subject.txt"  

body_words = read_words_from_file(file_path_body)
subject_words = read_words_from_file(file_path_subject)

with open(file, 'r') as f: 
    data = json.load(f)

for email in data['emails']:

    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = email.strip()
    msg["Subject"] = subject_words
    msg.set_content(body_words)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"✅ {email}")
    except Exception as e:
        print(f"❌ {email} : {e}")