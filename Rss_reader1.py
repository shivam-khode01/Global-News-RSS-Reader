from flask import Flask, jsonify, request
import feedparser
import requests
from langdetect import detect
import time
from datetime import datetime, timedelta
import pandas as pd
import os

app = Flask(__name__)

rss_feeds = {
    "UK": {"BBC": "http://feeds.bbci.co.uk/news/rss.xml"},
    "USA": {"CNN": "http://rss.cnn.com/rss/edition.rss"},
    "India": {"The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss"},
    "Japan": {"NHK": "https://www3.nhk.or.jp/rss/news/cat0.xml"},
    "Germany": {"DW": "https://rss.dw.com/rdf/rss-en-all"},
    "China": {"Xinhua": "http://www.xinhuanet.com/english/rss/worldrss.xml"},
    "Australia": {"ABC": "https://www.abc.net.au/news/feed/51120/rss.xml"},
    "South Korea": {"KBS": "https://world.kbs.co.kr/rss/rss_news.htm?lang=e"},
    "Russia": {"RT": "https://www.rt.com/rss/news/"},
    "Italy": {"ANSA": "https://www.ansa.it/sito/ansait_rss.xml"},
    "Spain": {"El Pais": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"},
    "France": {"Le Monde": "https://www.lemonde.fr/rss/une.xml"},
    "Canada": {"Global News": "https://globalnews.ca/feed/"},
    "Brazil": {"Estadao": "https://www.estadao.com.br/rss/ultimas.xml"},
    "Mexico": {"Proceso": "https://www.proceso.com.mx/feed"},
    "South Africa": {"IOL": "https://www.iol.co.za/cmlink/1.640"},
    "Singapore": {"Straits Times": "https://www.straitstimes.com/news/world/rss.xml"},
    "Indonesia": {"Kompas": "https://indeks.kompas.com/headline.rss"},
    "Malaysia": {"The Star": "https://www.thestar.com.my/rss/editors-choice"},
    "UAE": {"Gulf News": "https://gulfnews.com/rss?generatorName=RSS-Feeds"},
    "Pakistan": {"Dawn": "https://www.dawn.com/feeds/home"},
    "Bangladesh": {"BDNews24": "https://bangla.bdnews24.com/rss.xml"},
    "Thailand": {"Bangkok Post": "https://www.bangkokpost.com/rss/data/topstories.xml"},
    "New Zealand": {"NZ Herald": "https://www.nzherald.co.nz/rss"},
    "Philippines": {"PhilStar": "https://www.philstar.com/rss/headlines"},
}

# Cache
cached_articles = []
last_fetched = None
CACHE_DURATION = timedelta(minutes=10)
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
                "country": country,
                "news_agency": agency,
                "title": title,
                "publication_date": published,
                "summary": summary,
                "news_url": link,
                "language": language
            })
        except Exception as e:
            print(f"Error parsing article from {agency} ({country}): {e}")
    return articles

def fetch_all_news():
    all_articles = []
    for country, agencies in rss_feeds.items():
        for agency, url in agencies.items():
            articles = parse_feed(country, agency, url)
            all_articles.extend(articles)
            time.sleep(1)

    # Remove duplicates
    unique = {}
    for art in all_articles:
        key = (art['title'], art['news_url'])
        unique[key] = art
    articles = list(unique.values())

    # Save to CSV and JSON
    df = pd.DataFrame(articles)
    df.to_csv(os.path.join(OUTPUT_DIR, "news_data.csv"), index=False, encoding="utf-8")
    df.to_json(os.path.join(OUTPUT_DIR, "news_data.json"), orient="records", force_ascii=False)

    return articles

@app.route('/news')
def get_news():
    global cached_articles, last_fetched

    if last_fetched is None or datetime.utcnow() - last_fetched > CACHE_DURATION:
        cached_articles = fetch_all_news()
        last_fetched = datetime.utcnow()

    country_filter = request.args.get('country', type=str)
    agency_filter = request.args.get('agency', type=str)
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=20, type=int)

    filtered = cached_articles
    if country_filter:
        filtered = [a for a in filtered if a['country'].lower() == country_filter.lower()]
        if not filtered:
            return jsonify({"error": f"No articles found for country '{country_filter}'"}), 404

    if agency_filter:
        filtered = [a for a in filtered if a['news_agency'].lower() == agency_filter.lower()]
        if not filtered:
            return jsonify({"error": f"No articles found for agency '{agency_filter}'"}), 404

    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    if start >= total:
        return jsonify({"error": "Page number out of range"}), 400

    paginated = filtered[start:end]
    return jsonify({
        "page": page,
        "page_size": page_size,
        "total_articles": total,
        "articles": paginated
    })

@app.route('/export/json')
def export_json():
    try:
        return open(os.path.join(OUTPUT_DIR, "news_data.json"), encoding="utf-8").read()
    except FileNotFoundError:
        return jsonify({"error": "JSON file not found"}), 404

@app.route('/export/csv')
def export_csv():
    try:
        return open(os.path.join(OUTPUT_DIR, "news_data.csv"), encoding="utf-8").read()
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
