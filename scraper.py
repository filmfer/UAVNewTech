import os
import requests
from datetime import datetime, timedelta
import time

# --- Config ---
API_KEY = os.getenv("GOOGLE_CSE_API_KEY")  # Replace with your API key
SITE_ID = os.getenv("GOOGLE_CSE_SITE_ID")   # Replace with your CSE ID (e.g., "YOUR_CSE_ID")
OUTPUT_FILE = "top_drone_incidents.txt"
TARGET_SEARCH_QUERIES = [
    "UAV drone LiDAR last month",
    "LiDAR agriculture last month",
    "forest fire detection drones last month",
    "agriculture remote sensing last month",
    "forest remote sensing management last month",
]

def fetch_google_results(query):
    """Fetch top 5 results from Google Custom Search API."""
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SITE_ID,  # Your CSE ID
        "q": query,
        "num": 5,
        "searchType": "web",
        "tbm": "isch",  # Optional: Add image search if needed
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def get_last_month_results():
    """Fetch all relevant results from the last month."""
    last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-01")
    current_date = datetime.now().strftime("%Y-%m-%d")

    with open(OUTPUT_FILE, "r+") as f:
        existing_links = set(line.strip() for line in f if line.strip())

    new_results = []
    for query in TARGET_SEARCH_QUERIES:
        results = fetch_google_results(query)
        for result in results:
            link = result.get("link")
            if link and link not in existing_links:
                new_results.append(link)

    return sorted(new_results, key=lambda x: datetime.strptime(x.split("/")[-1].split("?")[0], "%Y-%m-%d"))

def main():
    """Run daily at 8 AM (Azores timezone)."""
    # Check if running in Azores timezone (~UTC+1)
    from pytz import timezone
    azores = timezone("Europe/Lisbon")
    now_azores = datetime.now(azores)

    if not now_azores.hour == 8:
        print(f"Skipping (not 8 AM in Azores). Current time: {now_azores}")
        return

    try:
        new_links = get_last_month_results()
        with open(OUTPUT_FILE, "a") as f:
            for link in new_links[:5]:  # Top 5
                f.write(link + "\n")
                print(f"Added: {link}")

        print("✅ Daily scrape completed!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
