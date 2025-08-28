#!/bin/bash

mkdir -p /root/SweetishPhish/logs

date=$(date +%F)     
day=$(date +%A | tr '[:upper:]' '[:lower:]')  

echo "Date: $date"
echo "Day: $day"

pwd

cd /root/SweetishPhish

max_searches_per_day= 
server_send_ratelimit= 
open_email_scraping_threads=30 
depth_per_url_search=2 #2 pages deep

export SMTP_URL=""
export SMTP_USER=""
export SMTP_PASS=""
export SERP_API_KEY="" 

#source env/bin/activate
source /root/SweetishPhish/env/bin/activate # add absoulte path

# <location_list_file.txt> <output_file_name> <keyword_list.txt> <excluded_list.txt> <site_filter.txt> <custom_inurl.txt> <max_searches_per_day> <serp_api_key>
python3 ./url_scraper.py ./dork_data/location_lists/$day.txt json_leads/$date.json ./dork_data/keyword_list.txt ./dork_data/excluded_list.txt ./dork_data/site_filter.txt ./dork_data/inurl_list.txt "$max_searches_per_day" "$SERP_API_KEY"

sleep 1

# python email_crawler.py -i <database file path> -o <output_results_file> -t <active_threads> -d <depth>
python3 email_crawler.py -i leads.db -o emails/$date.json -t "$open_email_scraping_threads" -d "$depth_per_url_search"

sleep 1

# python controller.py <Server URL> <SMTP username> <SMTP Password> <rate limit>
python3 ./controller.py "$SMTP_URL" "$SMTP_USER" "$SMTP_PASS" "$server_send_ratelimit"

# make sure its a executable - chmod +x run_pipeline.sh
