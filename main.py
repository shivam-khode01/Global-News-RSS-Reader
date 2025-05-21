import feedparser
import pandas as pd
from datetime import datetime
from langdetect import detect
import time
import os
import requests


# RSS Feeds from 20+ Countries

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

# Parse a Single RSS Feed

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


# Collect All Articles

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


# Save to CSV and JSON

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

# Summary Table 

# Create new DataFrame for formatted summary table
summary_data = []

# Process each country
for country, agencies in rss_feeds.items():
    country_data = df[df["Country"] == country]
    
    if not country_data.empty:
        # Get all unique news agencies for this country
        agencies_list = ", ".join(sorted(country_data["News Agency"].unique()))
        
        # Get article count
        article_count = len(country_data)
        
        # Format article count with "m" suffix if over 1 million
        formatted_count = f"{article_count/1000000:.1f}m" if article_count >= 1000000 else str(article_count)
        
        # Get earliest publication date
        if not country_data["Publication Date"].empty:
            try:
                # Try to parse dates and find the earliest
                dates = pd.to_datetime(country_data["Publication Date"], errors="coerce")
                earliest_date = dates.min()
                if pd.notna(earliest_date):
                    # Format as "Since YYYY"
                    historical_data = f"Since {earliest_date.year}"
                else:
                    historical_data = "N/A"
            except:
                historical_data = "N/A"
        else:
            historical_data = "N/A"
        
        # Add to summary data
        summary_data.append({
            "Country": country,
            "News Agency": agencies_list,
            "Total articles downloaded": formatted_count,
            "Total historical data": historical_data
        })

# Create the summary DataFrame
summary_df = pd.DataFrame(summary_data)

# Save formatted summary table in both CSV and JSON formats
summary_csv_path = os.path.join(output_dir, "news_summary_formatted.csv")
summary_json_path = os.path.join(output_dir, "news_summary_formatted.json")

# Save to CSV
summary_df.to_csv(summary_csv_path, index=False)
print(f"Formatted summary saved to CSV: {summary_csv_path}")

# Save to JSON
summary_df.to_json(summary_json_path, orient="records", force_ascii=False)
print(f"Formatted summary saved to JSON: {summary_json_path}")

# Display the formatted summary table
print("\nFormatted Summary Table:")
print(summary_df.to_string(index=False))
