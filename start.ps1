$date = (Get-Date).ToString("yyyy-MM-dd")
$day = (Get-Date).DayOfWeek.ToString().ToLower()

Write-Output $date
Write-Output $day

Get-Location

$max_searches_per_day = 
$server_send_ratelimit = 
$open_email_scraping_threads = 30 
$depth_per_url_search = 2 #2 pages deep

$env:SerpAPIkey = ""
$env:SMTP_USER = ""
$env:SMTP_PASS = ""
$env:SMTP_URL = "smtp.mailgun.org"
# <location_list_file.txt> <output_file_name> <keyword_list.txt> <excluded_list.txt> <site_filter.txt> <custom_inurl.txt> <max_searches_per_day> <serp_api_key>
python .\url_scraper.py .\dork_data\location_lists\$day.txt json_leads\$date.json .\dork_data\keyword_list.txt .\dork_data\excluded_list.txt .\dork_data\site_filter.txt .\dork_data\inurl_list.txt $max_searches_per_day $env:SerpAPIkey

Start-Sleep -Seconds 1

python email_crawler.py -i leads.db -o emails\$date.json -t $open_email_scraping_threads -d $depth_per_url_search

Start-Sleep -Seconds 1

# python controller.py <Server URL> <SMTP username> <SMTP Password> <rate limit>
python .\controller.py $env:SMTP_URL $env:SMTP_USER $env:SMTP_PASS $server_send_ratelimit