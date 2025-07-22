#!/bin/bash

date=$(date +%F)     
day=$(date +%A | tr '[:upper:]' '[:lower:]')  

echo "Date: $date"
echo "Day: $day"

pwd

export SERP_API_KEY=""

# python url_scraper <location_list_file.txt> <output_file_name> <keyword_list.txt> <excluded_list.txt> <site_filter.txt> <custom_inurl.txt> <Serp-API-Key>
python3 ./url_scraper.py ./dork_data/location_lists/$day.txt json_leads/$date.json ./dork_data/keyword_list.txt ./dork_data/excluded_list.txt ./dork_data/site_filter.txt ./dork_data/inurl_list.txt "$SERP_API_KEY"

sleep 1

# python email_crawler.py -i output_json/7_1.json -o results.json -t 30 -d 2
python3 email_crawler.py -i json_leads/$date.json -o emails/$date.json -t 30 -d 2

sleep 1

export SMTP_URL=""
export SMTP_USER=""
export SMTP_PASS=""

# python controller.py <Server URL> <SMTP username> <SMTP Password> <date>
python3 ./controller.py "$SMTP_URL" "$SMTP_USER" "$SMTP_PASS" "$date"

# make sure its a executable - chmod +x run_pipeline.sh
