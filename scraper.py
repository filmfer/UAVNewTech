import requests
from datetime import datetime, timedelta
import os

# --- Config ---
API_KEY = os.getenv("GOOGLE_CSE_API_KEY")  # From GitHub Secrets
CX = os.getenv("GOOGLE_CSE_SITE_ID")      # From GitHub Secrets
QUERY_1 = "drone UAV safety incidents"
QUERY_2 = "Lidar malfunctions in agriculture"
QUERY_3 = "forest fire detection drone failures"
QUERY_4 = "remote sensing agriculture accidents"

# --- Fetch Google Search Results ---
def fetch_google_results(query, month_back=30):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"
    params = {"dateRestrict": f"{datetime.now() - timedelta(days=month_back)}"}
    response = requests.get(url, params=params)
    return response.json()

# --- Scrape Top 5 Results ---
def scrape_top_results(query):
    results = fetch_google_results(query)
    if not results or "items" not in results:
        print(f"No results for: {query}")
        return []

    # Extract top 5 links
    top_links = []
    for item in results["items"][:5]:
        top_links.append(item.get("link", ""))

    return top_links

# --- Main Execution ---
if __name__ == "__main__":
    queries = [QUERY_1, QUERY_2, QUERY_3, QUERY_4]
    all_results = {}

    for query in queries:
        print(f"Searching: {query}")
        results = scrape_top_results(query)
        all_results[query] = results

    # --- Save to Text File ---
    filename = "top_drone_incidents.txt"
    with open(filename, "w") as f:
        for query, links in all_results.items():
            f.write(f"=== {query} ===\n")
            for link in links[:5]:
                f.write(link + "\n\n")

    print(f"Saved results to: {filename}")
