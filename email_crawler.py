import requests
from bs4 import BeautifulSoup
import re
import argparse
import json
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from requests.exceptions import RequestException, Timeout, ConnectionError
import sqlite3
import os



base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "leads.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visited_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    source_website TEXT,
    date_scraped TEXT DEFAULT (datetime('now'))
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT UNIQUE,
    date_scraped TEXT DEFAULT (datetime('now'))
)
""")
conn.commit()

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

visited_urls = set()
visited_lock = threading.Lock()

emails_found = set()
emails_lock = threading.Lock()

MAX_RETRIES = 3


def log_url(source_url, visited_url):
    with sqlite3.connect(db_path) as conn_local:
        cursor = conn_local.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO visited_urls (url, source_website)
            VALUES (?, ?)
        """, (visited_url, source_url))
        conn_local.commit()


def log_email(email):
    with sqlite3.connect(db_path) as conn_local:
        cursor = conn_local.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO emails (email)
            VALUES (?)
        """, (email,))
        conn_local.commit()



def get_html(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
            resp.raise_for_status()
            print(f"[Fetched] {resp.url}")
            return resp.text
        except (Timeout, ConnectionError):
            print(f"[Timeout] {url} (attempt {attempt}/{MAX_RETRIES})")
        except RequestException as e:
            print(f"[Error] {url} → {e}")
            break
    return ""

def extract_emails(html):
    soup = BeautifulSoup(html, 'html.parser')
    emails = set()

    for tag in soup.find_all('a', href=True):
        if tag['href'].startswith('mailto:'):
            email = tag['href'][7:].split('?')[0].strip('.')
            emails.add(email)

    text = soup.get_text()
    emails.update(re.findall(EMAIL_REGEX, text))

    return emails

def extract_absolute_urls(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        absolute_url = urljoin(base_url, href)
        if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
            urls.add(absolute_url)
    return urls

def crawl_url(url, base_url, depth, max_depth, executor, to_visit):
    with visited_lock:
        if url in visited_urls:
            return
        visited_urls.add(url)

    log_url(base_url, url)

    html = get_html(url)
    if not html:
        return

    found = extract_emails(html)
    with emails_lock:
        emails_found.update(found)

    for email in found:
        log_email(email)

    if depth < max_depth:
        links = extract_absolute_urls(url, html)
        for link in links:
            with visited_lock:
                if link not in visited_urls:
                    future = executor.submit(crawl_url, link, base_url, depth + 1, max_depth, executor, to_visit)
                    to_visit.append(future)

def crawl_website(start_url, max_depth=2, max_threads=20):
    visited_urls.clear()
    emails_found.clear()
    to_visit = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future = executor.submit(crawl_url, start_url, start_url, 0, max_depth, executor, to_visit)
        to_visit.append(future)
        for _ in as_completed(to_visit):
            pass

    return emails_found

def extract_url(line):
    line = line.strip()
    match = re.search(r'(https?://[^\s]+|www\.[^\s]+)', line)
    if match:
        url = match.group(0)
        if url.startswith("www."):
            url = "http://" + url
        return url
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="File containing list of URLs to crawl (one per line, with or without numbering)")
    parser.add_argument("-o", "--output", default="output.json", help="Output JSON filename")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of concurrent threads (default: 20)")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Depth of crawling (default: 2)")
    args = parser.parse_args()

    all_emails = set()

    with open(args.input, 'r') as infile:
        urls = set()# same as a list but avoids duplicates
        data = json.load(infile)
        for state, firms in data.items():
                print(f"Looping through {state}...")
                for firm in firms:
                    link = firm.get("link")
                    urls.add(link)


    for url in urls:
        print(f"\n🔎 Starting crawl on: {url}")
        found = crawl_website(url, max_depth=args.depth, max_threads=args.threads)
        all_emails.update(found)

    result = {"emails": sorted(all_emails)}

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Crawling complete! Found emails: {result['emails']}")
    print(f"Results saved to {args.output}")

conn.close()


# python email_crawler.py -i output_json/7_1.json -o results.json -t 30 -d 2
# python email_crawler.py -i output_json/7_1.json -o results.json
