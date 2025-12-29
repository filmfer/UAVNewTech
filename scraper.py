import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# --- Constants ---
SEARCH_KEYWORDS = [
    "drone UAV safety incidents",
    "Lidar malfunctions in agriculture",
    "forest fire detection drone failures",
    "remote sensing agriculture accidents"
]
API_KEY = os.getenv("GOOGLE_CSE_API_KEY")  # Set this in GitHub Secrets
CSE_ID = os.getenv("GOOGLE_CSE_ID")        # Set this in GitHub Secrets

def fetch_google_search(query, month_back=1):
    """Fetch Google search results using CSE API."""
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Filter for last month
        current_month = datetime.now().month
        one_month_ago = (datetime.now() - timedelta(days=30)).replace(hour=0, minute=0, second=0)

        results = []
        for item in data.get("items", []):
            if "datePublished" in item:
                published_date = datetime.strptime(item["datePublished"], "%Y-%m-%d")
                if current_month >= one_month_ago.month or (current_month == one_month_ago.month and published_date.day >= one_month_ago.day):
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "description": item.get("snippet", "")
                    })
        return results
    except Exception as e:
        print(f"Error fetching Google search: {e}")
        return []

def scrape_drone_incidents():
    """Scrape top 5 major incidents from last month."""
    all_results = []
    for keyword in SEARCH_KEYWORDS:
        results = fetch_google_search(keyword)
        all_results.extend(results)

    # Remove duplicates (by link) and sort by date
    unique_results = []
    seen_links = set()

    for result in all_results:
        if result["link"] not in seen_links:
            seen_links.add(result["link"])
            unique_results.append(result)

    # Sort by date (newest first)
    unique_results.sort(key=lambda x: datetime.strptime(x.get("datePublished", ""), "%Y-%m-%d"), reverse=True)

    return unique_results[:5]

def save_to_file(results, filename="top_drone_incidents.txt"):
    """Save results to a text file."""
    try:
        with open(filename, "w") as f:
            for i, result in enumerate(results, 1):
                f.write(f"{i}. {result['title']}\n")
                f.write(f"   Link: {result['link']}\n")
                f.write(f"   Description: {result['description']}\n\n")

        print("✅ Results saved successfully.")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def check_for_new_content(filename):
    """Check if new content was added since last run."""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        # Check if any link from today exists
        current_date = datetime.now().strftime("%Y-%m-%d")
        has_today_links = any(
            line.strip().startswith("1. ") and current_date in line
            for line in lines
        )

        return not has_today_links
    except Exception as e:
        print(f"❌ Error checking file: {e}")
        return False

def main():
    """Main execution."""
    try:
        results = scrape_drone_incidents()
        if not results:
            print("⚠️ No results found.")
            return False  # GitHub Actions will skip commit

        save_to_file(results)
        filename = "top_drone_incidents.txt"
        needs_commit = check_for_new_content(filename)

        if needs_commit:
            print("📤 New content detected. Commit changes.")
            return True
        else:
            print("⏳ No new content since last run.")
            return False

    except Exception as e:
        print(f"❌ Script failed: {e}")
        return False

if __name__ == "__main__":
    main()
