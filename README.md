# Global News RSS Reader

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A multi-country news aggregator that collects headlines and summaries from RSS feeds across 20+ countries. This project saves news data to JSON and CSV files and provides a Flask API for accessing the news with filtering and pagination capabilities.

## 📋 Features

- ✅ Fetches news articles from multiple international RSS feeds
- 🌍 Detects the language of each article summary
- 💾 Saves aggregated data to both JSON and CSV files simultaneously
- 🔄 Removes duplicate articles based on title and URL
- 📊 Enhanced summary data available in both CSV and JSON formats
- 📈 Formatted summary with article counts and historical data ranges
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
- `news_summary_formatted.csv` - Formatted statistical summary by country (CSV)
- `news_summary_formatted.json` - Formatted statistical summary by country (JSON)

### Summary Table Format

The formatted summary tables provide an easy-to-read overview with the following columns:

| Country | News Agency | Total articles downloaded | Total historical data |
|---------|------------|---------------------------|----------------------|
| Country 1 | A, B, C | 1m | Since 2021 |
| Country 2 | ... | ... | ... |

- **Total articles downloaded**: Shows count with "m" suffix for counts over 1 million
- **Total historical data**: Shows range as "Since YYYY" based on earliest publication date

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
| `/summary/json` | Download formatted summary data as JSON | None |
| `/summary/csv` | Download formatted summary data as CSV | None |

Example requests:
```bash
http://localhost:5000/news?country=India&page=2&page_size=10
http://localhost:5000/news?agency=CNN
http://localhost:5000/summary/json
```

## 🔍 Notes & Considerations

- Some RSS feeds may fail occasionally due to network issues or feed URL changes
- Language detection may misclassify short or ambiguous summaries
- Polite delay (`time.sleep(1)`) added between requests to avoid overwhelming servers
- Flask API caches results for 10 minutes to reduce load and improve response times

## ✨ Bonus Features

- **Enhanced Summary Format**: Stylized summary tables with clean formatting
- **Dual Format Exports**: All data available in both JSON and CSV formats
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

For Windows users, use Task Scheduler with a daily trigger to run the script.

## 📊 Sample Output

### Summary Table Example

```
|-------------|--------------|--------------------------|-------------------|
| Country     | News Agency  | Total articles downloaded| Total historical  |
|-------------|--------------|--------------------------|-------------------|
| UK          | BBC          | 1.2m                     | Since 2021        |
| USA         | CNN          | 856                      | Since 2022        |
| Japan       | NHK          | 345                      | Since 2023        |
| ...         | ...          | ...                      | ...               |
|-------------|--------------|--------------------------|-------------------|
```
