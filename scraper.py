import os
import logging
from datetime import datetime, timedelta
import requests
from typing import List

# --- Constants ---
API_KEY = "AIzaSyD1XGZTfeL2esGXDe2v9xYt8KuVvO4ZfAo"  # Replace with your actual API key
CSE_ID = "23d8dd8f6aa574750"  # Replace with your CSE ID
OUTPUT_FILE = "top_drone_remote_sensing_links.txt"
TOPICS = [
    "drone UAV lidar agriculture forests remote sensing",
    "UAV lidar forest monitoring",
    "agriculture drone LiDAR",
    "forest fire detection with drones",
    "remote sensing agriculture"
]
RATE_LIMIT_DELAY = 1.0  # Seconds between requests

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

def log_error(message: str) -> None:
    """Log errors to 'scraper.log'."""
    logging.error(f"ERROR: {message}")

class GoogleSearchScraper:
    def __init__(self):
        self.session = requests.Session()

    def fetch_results(self, query: str, start_date: str = None, end_date: str = None) -> List[str]:
        """Fetch top 5 results from Google Custom Search API."""
        params = {
            "q": query,
            "key": API_KEY,
            "cx": CSE_ID,
            "num": 5,
        }

        if start_date or end_date:
            params["startDate"] = start_date
            params["endDate"] = end_date

        try:
            response = self.session.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            # Extract unique URLs from results
            urls = []
            for item in data.get("items", []):
                if "link" in item:
                    urls.append(item["link"])

            return list(set(urls))[:5]  # Remove duplicates, top 5

        except requests.exceptions.RequestException as e:
            log_error(f"Failed to fetch Google results: {e}")
            return []
        except Exception as e:
            log_error(f"Unexpected error: {e}")
            return []

    def get_last_month_results(self) -> List[str]:
        """Fetch search results for the last 30 days."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        all_links = []
        for topic in TOPICS:
            try:
                time.sleep(RATE_LIMIT_DELAY / len(TOPICS))  # Distribute delay
                results = self.fetch_results(
                    query=topic,
                    start_date=start_date,
                    end_date=end_date
                )
                all_links.extend(results)

            except Exception as e:
                log_error(f"Failed to scrape {topic}: {e}")

        return list(set(all_links))[:5]  # Remove duplicates, top 5

def save_results_to_file(links: List[str]) -> None:
    """Append new links to OUTPUT_FILE."""
    with open(OUTPUT_FILE, "a") as f:
        for link in links:
            f.write(f"{link}\n")

def main():
    """Main execution function."""
    scraper = GoogleSearchScraper()

    # Check if we should run (8 AM Azores time)
    azores_timezone = datetime.now() - timedelta(hours=1)  # UTC-1
    if not (7.5 <= azores_timezone.hour < 9):  # ~8 AM in Azores
        log_error("Skipping: Not running at 8 AM Azores time.")
        return

    try:
        new_links = scraper.get_last_month_results()
        save_results_to_file(new_links)

        logging.info(f"Successfully saved {len(new_links)} links to {OUTPUT_FILE}")

    except Exception as e:
        log_error(f"Critical error: {e}")

if __name__ == "__main__":
    main()
