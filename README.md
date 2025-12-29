# UAVNewTech
Top 5 major outbreaks related to drones, LiDAR, and agriculture/forest remote sensing from the last month.

# Drone Remote Sensing Scraper

A Python script that scrapes Google Custom Search for top 5 major outbreaks related to drones, LiDAR, and agriculture/forest remote sensing from the last month.

## Features
- Runs daily at ~8 AM Azores time (UTC-1)
- Automatically handles winter/summer daylight changes
- Saves results to `top_drone_remote_sensing_links.txt`
- Logs errors to `scraper.log`

## Setup

### Prerequisites
- Python 3.10+
- Google Custom Search API key
- CSE ID from Google Cloud Console

### Configuration
1. Replace `YOUR_GOOGLE_CSE_API_KEY` and `YOUR_CUSTOM_SEARCH_ENGINE_ID` in `scraper.py`
2. Add these secrets to your GitHub repository:
   - `GOOGLE_API_KEY`
   - `CUSTOM_SEARCH_ENGINE_ID`

### Deployment
1. Push the code to a GitHub repository
2. Enable the workflow in `.github/workflows/daily-scrape.yml`
3. The script will run automatically on schedule

## Output
- Daily results saved to `top_drone_remote_sensing_links.txt`
- Logs stored in `scraper.log`

## License
MIT
