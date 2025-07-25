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

```
./start.sh
```
- activates the script

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


