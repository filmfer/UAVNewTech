import os
from datetime import datetime, timedelta

# --- Configuration ---
FILE_PATH = "top_drone_remote_sensing_links.txt"
DAYS_TO_KEEP = 90  # How many days of history to keep (e.g., 3 months)

def run_cleanup():
    """
    Reads the data file, removes entries older than DAYS_TO_KEEP, 
    and saves the cleaned version back to the file.
    """
    if not os.path.exists(FILE_PATH):
        print("⚠️ File not found. Nothing to clean.")
        return

    print(f"🧹 Starting cleanup (Threshold: {DAYS_TO_KEEP} days)...")
    
    # Read the entire file content
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # The separator used in your scraper script
    separator = "-" * 40
    
    # Split content into individual entry blocks
    # We strip empty strings in case of trailing newlines
    blocks = [b.strip() for b in content.split(separator) if b.strip()]
    
    total_entries = len(blocks)
    kept_blocks = []
    removed_count = 0
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP)

    for block in blocks:
        # Extract the date line from the block
        lines = block.split('\n')
        date_line = next((line for line in lines if "Date Scraped:" in line), None)
        
        should_keep = True
        
        if date_line:
            try:
                # Parse the date string (e.g., "2026-01-02")
                date_str = date_line.split("Date Scraped:")[1].strip()
                entry_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                # Check if the entry is too old
                if entry_date < cutoff_date:
                    should_keep = False
                    removed_count += 1
            except ValueError:
                # If date parsing fails, keep the entry just in case
                print(f"⚠️ Could not parse date in block: {block[:30]}...")
                should_keep = True

        if should_keep:
            kept_blocks.append(block)

    # If nothing changed, exit
    if removed_count == 0:
        print("✅ No old entries found. File is clean.")
        return

    # Reconstruct the file content
    # We add the separator and a newline back to each block
    new_content = ""
    for block in kept_blocks:
        new_content += block + "\n" + separator + "\n"

    # Overwrite the file with the cleaned data
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"♻️ Cleanup complete: Removed {removed_count} entries. Kept {len(kept_blocks)} entries.")

if __name__ == "__main__":
    run_cleanup()
