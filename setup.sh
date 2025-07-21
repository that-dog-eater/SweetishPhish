#!/bin/bash

echo Cloning Git repo

REPO="that-dog-eater/SweetishPhish" #Change this with the correct Repo name

latest_tag=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep "tag_name" | cut -d '"' -f4)

wget https://github.com/$REPO/archive/refs/tags/$latest_tag.zip -O release.zip

unzip release.zip
cd $REPO-*  


echo Creating Dirs and Files for setup...

mkdir -p dork_data/location_lists

touch dork_data/excluded_list.txt
touch dork_data/inurl_list.txt
touch dork_data/keyword_list.txt
touch dork_data/site_filter.txt

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



