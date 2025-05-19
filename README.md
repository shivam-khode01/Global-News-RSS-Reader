# Global News RSS Reader

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A multi-country news aggregator that collects headlines and summaries from RSS feeds across 20+ countries. This project saves news data to JSON and CSV files and provides a Flask API for accessing the news with filtering and pagination capabilities.

## 📋 Features

- ✅ Fetches news articles from multiple international RSS feeds
- 🌍 Detects the language of each article summary
- 💾 Saves aggregated data to both JSON and CSV files simultaneously
- 🔄 Removes duplicate articles based on title and URL
- 📊 Provides a summary CSV with counts per country
- 🌐 **Bonus:** Flask API with pagination and filters
- ⬇️ **Bonus:** API endpoints to export JSON and CSV files directly

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shivam-khode01/Global-News-RSS-Reader.git
   cd Global-News-RSS-Reader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Standalone News Fetcher

Run the main script to fetch news and save to files:

```bash
python main.py
```

Output files are saved in the `output/` directory:
- `news_data.json` - All news articles in JSON format
- `news_data.csv` - All news articles in CSV format
- `news_summary.csv` - Statistical summary by country

### Flask API

Start the API server:

```bash
python Rss_reader1.py
```

By default, the API runs on http://localhost:5000

#### API Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/news` | Get paginated news articles | `country`, `agency`, `page`, `page_size` |
| `/export/json` | Download complete news data as JSON | None |
| `/export/csv` | Download complete news data as CSV | None |

Example requests:
```bash
http://localhost:5000/news?country=India&page=2&page_size=10
http://localhost:5000/news?agency=CNN
```

## 🔍 Notes & Considerations

- Some RSS feeds may fail occasionally due to network issues or feed URL changes
- Language detection may misclassify short or ambiguous summaries
- Polite delay (`time.sleep(1)`) added between requests to avoid overwhelming servers
- Flask API caches results for 10 minutes to reduce load and improve response times

## ✨ Bonus Features

- **API Integration:** Easy querying with filters and direct file export
- **Smart Pagination:** Navigate through large datasets efficiently
- **Performance Caching:** Minimizes repeated RSS downloads

## ⏱️ Automation (Optional)

To run the fetcher daily with cron (Linux/macOS):

```bash
crontab -e
```

Add the following line to run at 6 AM daily:

```bash
0 6 * * * /usr/bin/python3 /full/path/to/main.py
```
