#!/bin/bash

echo Creating Dirs and Files for setup...

mkdir -p dork_data/location_lists

touch dork_data/excluded_list.txt
printf "linkedin\nindeed\nyelp\nclutch\ntop\nlist\ndirectory\nziprecruiter\nfacebook\nbizjournal" > dork_data/excluded_list.txt

touch dork_data/inurl_list.txt
printf "inurl:about\ninurl:services\ninurl:contact" > dork_data/inurl_list.txt

touch dork_data/keyword_list.txt

touch dork_data/site_filter.txt
printf "site:.com" > dork_data/site_filter.txt

touch dork_data/location_lists/sunday.txt
touch dork_data/location_lists/monday.txt
touch dork_data/location_lists/tuesday.txt
touch dork_data/location_lists/wednesday.txt
touch dork_data/location_lists/thursday.txt
touch dork_data/location_lists/friday.txt
touch dork_data/location_lists/saturday.txt


mkdir -p emails/templates

touch emails/templates/body.txt
touch emails/templates/subject.txt


mkdir json_leads



