# SweetishPhish

## Create Enviornment
  
install
```
sudo apt update
sudo apt install tmux -y
```
Create Session
```
 tmux new -s phishing 
```
- Ctrl + b, then release both keys and press d  
- (tmux attach -t mysession) - to connect  

Clone Repo
```
git clone --branch main --single-branch https://github.com/that-dog-eater/SweetishPhish.git
```
- cd into the dir created


Permissions
```
chmod +x setup.sh
chmod +x start.sh
```

Create Python Env
```
sudo apt update
sudo apt install python3 python3-venv -y
```
```
python3 -m venv env
```
```
source env/bin/activate
```

Install Python Dependencies
```
pip install requests beautifulsoup4 serpapi
pip install google-search-results
```

Create Cron job to run Daily
```
	crontab -e
```
- Select Nano if prompted
```
0 8 * * * /bin/bash /root/SweetishPhish/start.sh >> /root/SweetishPhish/logs/cron.log 2>&1
```
```
crontab -l (to verify)
```
## Script Config

1. Add Keywords to dork_data/Keywords.txt for dorking
2. Edit emails/templates/body.txt and subject.txt for email config  
3. Edit each day under dorkdata/location_lists
- add a place to search with a line break for each new place
- EX
  - Delaware
  - New York
4. Edit Start.sh and add the mailgun relays creds into it and serpapi key
5. Change Rate limiting in start.sh (defulat: set to 300)
6. Adjust Sending delay in controller (defulat: 300 - 600 seconds)

```
./setup.sh
```
```
./start.sh
```
- activates the script

## Verification Site
This is used so if your account gets flagged by Mailgun you can get it unbanned. A link to your Terms of Service must also be added at the bottom of the email to avoid bans.

**Prerequisites**
- Domain
- Cloudflare account 
- Cloudflare pages account
- Static site (index.html, stylesheet.css, etc)
  	- Download this from the Verification Folder in Main branch
 
**Instructions**
1. Cloudflare Pages create project
	- Manual upload
2. add files follow directions
3. click add domain
4. follow directions 
5. add nameservers to Domain provider (namecheap)
6. transfer DNS
7. in Cloudflare project that hosts the site press setup Domain
8. copy and paste dns cname into the dns nameserver cloudflare dashboard.
9. Wait to say active

## Mailgun / Namecheap Config

1. Add domain to Mailgun (dont use a subdomain when adding)
2. Setup DNS records on Cloudflare for Mailgun
	- CNAME records = turn off proxy through cloudflare
3. Add a smtp user
   - SMTP Credentials > add new SMTP user
   - Save user and password
5. Create the Reply designated Gmail account
6. In the Reply designated Gmail account add fowarding to the mailgun server
	- Go to settings > Accounts and imports > send mail as > add another email address
	- in the yellow box - Name: normal (max) , Email: domain (max@thisisaexample.com)
	- enter SMTP server, username, password avalible under SMTP credentials in mailgun
	- Set as defualt sending address
7. In mailgun add a catch all request to foward all emails back to the reply designated email
8. send the verification to allow gmail to send emails through that server and recive it in the same inbox
9. Finish the Start.sh Config
10. DONE!  
```
Scirpt -> mailgun -> clinet
reply -> mailgun -> gmail inbox
Gmail inbox -> mailgun -> Client
```

## Requirments:
- requests
- beautifulsoup4
- serpapi
- google-search-results
- dns.resolver
- random


