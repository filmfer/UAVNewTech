import os
import requests
from datetime import datetime, timedelta
import logging
from googleapiclient.discovery import build

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

def get_google_search_results(query, max_results=5):
    """Fetch search results from Google Custom Search API"""
    try:
        # Get secrets from environment variables
        api_key = os.getenv('GOOGLE_API_KEY')
        cse_id = os.getenv('CUSTOM_SEARCH_ENGINE_ID')

        if not api_key or not cse_id:
            raise ValueError("Missing required Google Custom Search API credentials")

        service = build('customsearch', 'v1', developerKey=api_key)

        # Calculate date range for last month
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Search query with date filter
        query_params = {
            'q': f"{query} site:google.com",
            'cx': cse_id,
            'startDate': start_date,
            'endDate': end_date,
            'num': max_results * 2,  # Get more results to filter by date
            'searchType': 'any'
        }

        response = service.cse().list(**query_params).execute()
        return response.get('items', [])

    except Exception as e:
        logging.error(f"Error fetching search results: {str(e)}")
        raise

def scrape_drone_related_outbreaks():
    """Scrape top 5 major outbreaks related to drones, LiDAR, and agriculture/forest remote sensing"""
    keywords = [
        "drone accidents",
        "LiDAR safety incidents",
        "agriculture drone malfunctions",
        "forest fire detection drones",
        "remote sensing failures"
    ]

    all_results = []
    for keyword in keywords:
        results = get_google_search_results(keyword)
        # Filter by date (last month) and add to our collection
        for item in results:
            if 'date' in item and datetime.strptime(item['date'], '%Y-%m-%d').year == datetime.now().year:
                all_results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'description': item.get('snippet', '')
                })

    # Sort by date (newest first) and return top 5 unique results
    unique_results = []
    seen_links = set()

    for result in all_results:
        if result['link'] not in seen_links:
            seen_links.add(result['link'])
            unique_results.append(result)

    # Sort by date (most recent first)
    unique_results.sort(key=lambda x: datetime.strptime(x.get('date', ''), '%Y-%m-%d'), reverse=True)

    return unique_results[:5]

def save_results_to_file(results, filename='top_drone_remote_sensing_links.txt'):
    """Save results to a text file"""
    try:
        with open(filename, 'w') as f:
            for i, result in enumerate(results, 1):
                f.write(f"{i}. {result['title']}\n")
                f.write(f"   Link: {result['link']}\n")
                f.write(f"   Description: {result['description']}\n\n")

        logging.info(f"Successfully saved {len(results)} results to {filename}")
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")
        raise

def check_for_new_content(filename):
    """Check if the output file has new content since last run"""
    try:
        # Get current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(filename, 'r') as f:
            lines = f.readlines()

        # Check if we have any links from today
        has_today_links = any(
            line.strip().startswith('1. ') and datetime.strptime(line.split('.')[0].split()[1], '%Y-%m-%d').year == datetime.now().year
            for line in lines
        )

        return not has_today_links

    except Exception as e:
        logging.error(f"Error checking file content: {str(e)}")
        raise False

def main():
    """Main execution function"""
    try:
        # Get search results
        logging.info("Starting drone related outbreak search...")
        results = scrape_drone_related_outbreaks()

        if not results:
            logging.warning("No relevant results found")
            return

        logging.info(f"Found {len(results)} relevant results")

        # Save to file
        save_results_to_file(results)

        # Check if we need to commit changes
        filename = 'top_drone_remote_sensing_links.txt'
        needs_commit = check_for_new_content(filename)

        if needs_commit:
            logging.info("New content found - committing changes")
            return True  # Indicate that GitHub Actions should commit

    except Exception as e:
        logging.error(f"Script failed: {str(e)}")

if __name__ == "__main__":
    main()
