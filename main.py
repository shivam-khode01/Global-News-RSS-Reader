import feedparser
import pandas as pd
from datetime import datetime
from langdetect import detect
import time
import os
import requests

# ---------------------------
# RSS Feeds from 20+ Countries
# ---------------------------
rss_feeds = {
    "UK": {"BBC": "http://feeds.bbci.co.uk/news/rss.xml"},
    "USA": {"CNN": "http://rss.cnn.com/rss/edition.rss"},
    "Middle East": {"Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml"},
    "Japan": {"NHK": "https://www3.nhk.or.jp/rss/news/cat0.xml"},
    "India": {"The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss"},
    "Singapore": {"CNA": "https://www.channelnewsasia.com/rssfeeds/8395986"},
    "Malaysia": {"Malay Mail": "https://www.malaymail.com/feed/rss"},
    "Indonesia": {"Jakarta Post": "https://www.thejakartapost.com/rss"},
    "South Korea": {"KBS": "https://world.kbs.co.kr/rss/rss_news.htm?lang=e"},
    "China": {"Xinhua": "http://www.xinhuanet.com/english/rss/worldrss.xml"},
    "Germany": {"DW": "https://rss.dw.com/rdf/rss-en-all"},
    "France": {"France24": "https://www.france24.com/en/rss"},
    "Australia": {"ABC": "https://www.abc.net.au/news/feed/51120/rss.xml"},
    "Canada": {"CBC": "https://www.cbc.ca/cmlink/rss-topstories"},
    "Russia": {"RT": "https://www.rt.com/rss/news/"},
    "Brazil": {"Folha": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"},
    "South Africa": {"News24": "https://www.news24.com/rss"},
    "Italy": {"ANSA": "https://www.ansa.it/sito/ansait_rss.xml"},
    "Spain": {"El Pais": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
    "Mexico": {"El Universal": "https://www.eluniversal.com.mx/rss.xml"},
}

# ---------------------------
# Parse a Single RSS Feed
# ---------------------------
def parse_feed(country, agency, url):
    articles = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"Failed to fetch {agency} ({country}): {e}")
        return []

    for entry in feed.entries:
        try:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            published = entry.get("published", "")
            link = entry.get("link", "")
            language = detect(summary) if summary else "unknown"

            articles.append({
                "Country": country,
                "News Agency": agency,
                "Title": title,
                "Publication Date": published,
                "Summary": summary,
                "News URL": link,
                "Language": language
            })
        except Exception as e:
            print(f"Error parsing article from {agency} ({country}): {e}")
    return articles

# ---------------------------
# Collect All Articles
# ---------------------------
all_articles = []

for country, agencies in rss_feeds.items():
    for agency, url in agencies.items():
        print(f"\nFetching: {agency} - {country}")
        try:
            articles = parse_feed(country, agency, url)
            all_articles.extend(articles)
            time.sleep(1)  # polite delay
        except Exception as e:
            print(f"Error processing {agency} ({country}): {e}")
            continue

# ---------------------------
# Save to CSV and JSON
# ---------------------------
df = pd.DataFrame(all_articles)
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

csv_path = os.path.join(output_dir, "news_data.csv")
json_path = os.path.join(output_dir, "news_data.json")

# Remove duplicates
df.drop_duplicates(subset=["Title", "News URL"], inplace=True)
df.to_csv(csv_path, index=False, encoding="utf-8")
df.to_json(json_path, orient="records", force_ascii=False)

print(f"\nSaved {len(df)} articles to {csv_path} and {json_path}")

# ---------------------------
# Summary Table (Enhanced Format)
# ---------------------------
summary_df = df.groupby(["Country"]).agg(
    News_Agencies=("News Agency", lambda x: ", ".join(sorted(set(x)))),
    Total_Articles=("Title", "count"),
    Earliest_Publication=("Publication Date", lambda x: min(x) if x.any() else "N/A")
).reset_index()

summary_df.rename(columns={
    "Country": "Country",
    "News_Agencies": "News Agency",
    "Total_Articles": "Total Articles Downloaded",
    "Earliest_Publication": "Total Historical Data"
}, inplace=True)

summary_path = os.path.join(output_dir, "news_summary.csv")
summary_df.to_csv(summary_path, index=False)
print(f"Summary saved to {summary_path}")

# ---------------------------
# (Optional) Cron Job Setup Hint (Linux/Mac)
# ---------------------------
# To schedule this script to run daily, you can add the following line to your crontab:
# Example (runs every day at 6 AM):
# 0 6 * * * /usr/bin/python3 /full/path/to/this_script.py
# Use `crontab -e` to edit and `crontab -l` to list current jobs.
# On Windows, use Task Scheduler with daily trigger.
