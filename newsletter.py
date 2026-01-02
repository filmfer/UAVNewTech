import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- Config ---
INPUT_FILE = "top_drone_remote_sensing_links.txt"
EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = "filmfer@gmail.com"

def parse_news_file():
    """Reads the text file and parses the top 5 most recent entries."""
    if not os.path.exists(INPUT_FILE):
        print(f"⚠️ Input file not found: {INPUT_FILE}")
        return []

    articles = []
    current_article = {}
    
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []
        
    # Process in reverse order to get the newest items first (assuming append-only file)
    for line in reversed(lines):
        line = line.strip()
        if "Link: " in line:
            current_article['link'] = line.split("Link: ")[1]
        elif "Snippet: " in line:
            current_article['summary'] = line.split("Snippet: ")[1]
        elif "Title: " in line:
            current_article['title'] = line.split("Title: ")[1]
        elif "Date Scraped: " in line:
            current_article['date'] = line.split("Date Scraped: ")[1]
        elif "----------------------------------------" in line:
            # End of a block defined by separator
            if 'title' in current_article and 'link' in current_article:
                articles.append(current_article)
            current_article = {}
            
    # Return top 5 most recent entries
    return articles[:5]

def determine_icon(title, summary):
    """
    Analyzes the title and summary text to select an appropriate emoji icon.
    Prioritizes Satellites, then Drones, then falls back to a generic dish.
    """
    # Combine text and convert to lowercase for easy searching
    combined_text = (str(title) + " " + str(summary)).lower()

    # Keywords to match against
    satellite_keywords = ['satellite', 'orbit', 'space agency', 'earth observation']
    drone_keywords = ['drone', 'uav', 'uas', 'quadcopter', 'fixed-wing', 'lidar', 'vtol']

    if any(keyword in combined_text for keyword in satellite_keywords):
        return "🛰️" # Satellite icon
    elif any(keyword in combined_text for keyword in drone_keywords):
        return "🚁" # Helicopter/Drone icon (represents quads/fixed-wing generic)
    else:
        # Default icon if no vehicle type is specifically mentioned (e.g., general agtech)
        return "📡" # Satellite Dish / Radar icon

def generate_html(articles):
    """Generates a modern, Canva-style HTML newsletter with dynamic icons."""
    
    html_header = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }}
            .container {{ max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.08); }}
            .header {{ background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%); color: #ffffff; padding: 35px 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 0.5px; }}
            .header p {{ margin: 12px 0 0; font-size: 15px; opacity: 0.9; font-weight: 300; }}
            .content {{ padding: 25px; background-color: #f8f9fa; }}
            .card {{ background: #ffffff; border-left: 5px solid #26d0ce; margin-bottom: 22px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: transform 0.2s; }}
            .card h2 {{ margin: 0 0 12px; font-size: 19px; color: #2c3e50; display: flex; align-items: center; }}
            .icon {{ font-size: 24px; margin-right: 10px; }}
            .card p {{ margin: 0 0 18px; color: #555; line-height: 1.6; font-size: 15px; }}
            .btn {{ display: inline-block; background-color: #1a2980; color: #ffffff !important; text-decoration: none; padding: 10px 18px; border-radius: 50px; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }}
            .footer {{ background-color: #2c3e50; color: #bdc3c7; text-align: center; padding: 25px; font-size: 13px; }}
            .footer p {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>UAV & Remote Sensing Weekly</h1>
                <p>Top 5 Insights for {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            <div class="content">
    """

    html_body = ""
    for article in articles:
        title = article.get('title', 'No Title')
        summary = article.get('summary', 'No summary available.')
        link = article.get('link', '#')
        
        # ✅ DYNAMIC ICON LOGIC HERE
        icon = determine_icon(title, summary)

        html_body += f"""
                <div class="card">
                    <h2><span class="icon">{icon}</span> {title}</h2>
                    <p>{summary}</p>
                    <a href="{link}" target="_blank" class="btn">READ FULL ARTICLE →</a>
                </div>
        """

    html_footer = """
            </div>
            <div class="footer">
                <p>Automated Agent by UAVNewTech</p>
                <p>Sent from Azores (UTC-1)</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_header + html_body + html_footer

def send_email(html_body):
    """Sends the email using Gmail SMTP."""
    msg = MIMEMultipart()
    msg['From'] = f"UAV News Agent <{EMAIL_SENDER}>"
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = f"🚀 Weekly Drone & LiDAR Report: {datetime.now().strftime('%Y-%m-%d')}"

    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Using Gmail's standard SMTP port and server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("❌ Error: EMAIL_USER or EMAIL_PASSWORD environment variables missing.")
        return

    print("📰 Parsing news file...")
    top_news = parse_news_file()
    
    if top_news:
        print(f"Found {len(top_news)} articles. Generating HTML...")
        email_html = generate_html(top_news)
        print(f"📧 Sending email to {EMAIL_RECEIVER}...")
        send_email(email_html)
    else:
        print("ℹ️ No news found in the text file to send. Skipping email.")

if __name__ == "__main__":
    main()
