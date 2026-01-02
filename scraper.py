import os
import requests
import logging
from datetime import datetime, timedelta

# --- Config ---
# Ensure these match the secrets in your GitHub Repo settings
API_KEY = os.getenv("GOOGLE_API_KEY") 
SITE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID") 

OUTPUT_FILE = "top_drone_remote_sensing_links.txt"
LOG_FILE = "scraper.log"

# Clean queries: Let the API handle the time filtering
TARGET_SEARCH_QUERIES = [
    "UAV drone Lidar outbreaks",
    "LiDAR agriculture technology",
    "forest fire detection drones",
    "agriculture remote sensing UAV",
    "forest remote sensing UAV",
]

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_google_results(query):
    """
    Fetch results from Google Custom Search API.
    Uses 'dateRestrict' to filter for the last month.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SITE_ID,
        "q": query,
        "num": 3,              
        # "searchType": "web",   <-- REMOVED (This caused the 400 Error)
        "dateRestrict": "m1",    # Keeps results to the last month
        # "sort": "date"         <-- REMOVED (relying on dateRestrict is safer)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # This raises errors for 400/500 codes
        data = response.json()
        
        if 'error' in data:
            logging.error(f"API Error for query '{query}': {data['error']}")
            return []
            
        return data.get("items", [])
    except Exception as e:
        # This catches the 400 error and logs it
        logging.error(f"Network error fetching '{query}': {e}")
        return []

def save_results(results):
    """
    Saves formatted results to the output file.
    Reads existing file to avoid duplicates.
    """
    # Load existing links to prevent duplicates
    existing_links = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if "Link: " in line:
                        existing_links.add(line.split("Link: ")[1].strip())
        except Exception as e:
            logging.warning(f"Could not read existing file: {e}")

    new_entries = []
    
    for item in results:
        link = item.get("link")
        title = item.get("title")
        snippet = item.get("snippet", "").replace("\n", " ")
        
        if link and link not in existing_links:
            # Create a formatted block for the text file
            entry = (
                f"Date Scraped: {datetime.now().strftime('%Y-%m-%d')}\n"
                f"Title: {title}\n"
                f"Snippet: {snippet}\n"
                f"Link: {link}\n"
                f"{'-'*40}\n"
            )
            new_entries.append(entry)
            existing_links.add(link) # Add to set to prevent dupes in same run

    if new_entries:
        try:
            # Prepend new results to the top of the file (optional, or append)
            # Here we append as per your original logic
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                for entry in new_entries:
                    f.write(entry)
            logging.info(f"Successfully added {len(new_entries)} new articles.")
            print(f"✅ Added {len(new_entries)} new articles.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")
    else:
        logging.info("No new unique links found.")
        print("ℹ️ No new unique links found.")

def main():
    if not API_KEY or not SITE_ID:
        print("❌ Error: Missing API_KEY or CUSTOM_SEARCH_ENGINE_ID environment variables.")
        return

    print("🚀 Starting Daily Scrape...")
    all_results = []
    
    for query in TARGET_SEARCH_QUERIES:
        print(f"Searching: {query}...")
        items = fetch_google_results(query)
        all_results.extend(items)
    
    # Optional: Deduplicate list based on link before processing
    unique_results = {v['link']: v for v in all_results}.values()
    
    save_results(unique_results)
    print("✅ Process complete.")

if __name__ == "__main__":
    main()
