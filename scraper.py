import os
import requests
from datetime import datetime, timedelta

# --- Config ---
API_KEY = os.getenv("GOOGLE_API_KEY")  # Replace with your API key
SITE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID")   # Replace with your CSE ID (e.g., "YOUR_CSE_ID")
OUTPUT_FILE = "top_drone_incidents.txt"
TARGET_SEARCH_QUERIES = [
    "UAV drone Lidar last month",
    "LiDAR agriculture last month",
    "forest fire detection drones last month",
    "agriculture remote sensing UAV",
    "forest remote sensing UAV",
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
    # Ensure output file exists
    with open(OUTPUT_FILE, "a+") as f:  # 'a+' mode ensures file is created if it doesn't exist
        pass

    existing_links = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            existing_links = {line.strip() for line in f}

    new_results = []
    for query in TARGET_SEARCH_QUERIES:
        results = fetch_google_results(query)
        for result in results:
            link = result.get("link")
            if link and link not in existing_links:
                new_results.append(link)

    return sorted(new_results, key=lambda x: datetime.strptime(x.split("/")[-1].split("?")[0], "%Y-%m-%d"))

def main():
    """Run daily scrape."""
    try:
        new_links = get_last_month_results()
        with open(OUTPUT_FILE, "a") as f:
            for link in new_links[:5]:
                f.write(link + "\n")
                print(f"Added: {link}")

        print("✅ Daily scrape completed!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
