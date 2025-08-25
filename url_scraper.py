from serpapi import GoogleSearch
import os
import json
import sqlite3
import sys
import datetime

if len(sys.argv) < 8:
    print("Usage: python script.py <location_list_file.txt> <output_file_name> <keyword_list.txt> <excluded_list.txt> <site_filter.txt> <custom_inurl.txt> <max_searches_per_day> <serp_api_key>")
    sys.exit(1)


Test_List = sys.argv[1]
Out_File_Name = sys.argv[2]
keyword_list = sys.argv[3]
excluded_list = sys.argv[4]
site_filter = sys.argv[5]
custom_inurl = sys.argv[6]
max_searches_per_day = int(sys.argv[7])
SerpAPIkey = sys.argv[8]

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "leads.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

today = datetime.date.today().isoformat()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    title TEXT,
    website TEXT UNIQUE,
    date_scraped TEXT
)

""")
conn.commit()


with open(Test_List, "r") as f:
    states = [line.strip() for line in f if line.strip()]

state_count = 0

for state in states:
    state_count += 1

searches_per_state = max_searches_per_day // state_count


all_results = {}

def is_new_url(cursor, website): # fix this once you create teh visited_urls Table
    cursor.execute("SELECT 1 FROM leads WHERE website = ?", (website,))
    return cursor.fetchone() is None

with open(keyword_list, "r") as f:
    keywords = [line.strip() for line in f if line.strip()]

with open(site_filter, "r") as f:
    site_filter = [line.strip() for line in f if line.strip()]

with open(custom_inurl, "r") as f:
    custom_inurl = [line.strip() for line in f if line.strip()]

with open(excluded_list, "r") as f:
    excluded_terms = [f"-{line.strip()}" for line in f if line.strip()]
excluded = " ".join(excluded_terms)


keywords_str = " OR ".join(keywords)
site_filter_str = " ".join(site_filter)
custom_inurl_str = " OR ".join(custom_inurl)




for state in states:
    print(state)

    page = 0
    max_pages = searches_per_state

    print(f'({keywords_str}) {state} ({site_filter_str}) ({custom_inurl_str}) {excluded}')
    
    while page < max_pages:

        print(page)


        params = {
            "engine": "google",
            "q": f'({keywords_str}) {state} ({site_filter_str}) ({custom_inurl_str}) {excluded}',
            "api_key": SerpAPIkey,
            "num": 100,
            "start" : page * 100
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        organic = results.get("organic_results", [])
        print(f"[{state}] Page {page+1} → {len(organic)} organic results")

        state_result = []

        for result in results.get("organic_results", []):
            title = result.get("title")
            website = result.get("link")

            if not title or not website:
                continue

            if is_new_url(cursor, website) == True:
            
                cursor.execute("""
                INSERT INTO leads (state, title, website, date_scraped)
                VALUES (?,?,?,?)
                """,(state, title, website, today))
                conn.commit()


                state_result.append({
                    "title": title,
                    "link": website
                })

                print(result.get("title"), "-", result.get("link"))

            else: 
                print(f"[SKIP] url already in database - {website}")

        if state_result:
                all_results[state] = state_result
        
        page += 1

conn.close()

with open(f"{Out_File_Name}", "w") as outfile:
    json.dump(all_results, outfile, indent=2)