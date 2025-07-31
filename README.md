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
- add a place to search wiht a line break for each new place
- EX
  - Delaware
  - New York
4. Edit Start.sh and add the mailgun relays creds into it
5. Change Rate limiting in start.sh (defulat: set to 300)
6. Adjust Sending delay in controller (defulat: 300 - 600 seconds)

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


1. Setup DNS records on Namecheap for Mailgun
2. Create the Reply designated Gmail account
3. TEMPORARY: Add a Catch-All request in Mailgun to foward all recieved emails to a temporary Gmail you control
4. In the Reply designated Gmail account add fowarding to the mailgun server
5. The temporary gmail should catch the fowarded verification code
6. Remove the Temporary Catch all request and change it to foward all replys to the Designated Reply Gmail
7. Finish the Start.sh Config
8. DONE!  
```
Scirpt -> mailgun -> clinet
reply -> mailgun -> gmail inbox
Gmail inbox -> mailgun -> Client 


