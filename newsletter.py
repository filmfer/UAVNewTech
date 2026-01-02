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
        return []

    articles = []
    current_article = {}
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Process in reverse to get the newest items first
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
            if 'title' in current_article:
                articles.append(current_article)
            current_article = {}
            
    # Return top 5 most recent
    return articles[:5]

def generate_html(articles):
    """Generates a modern, Canva-style HTML newsletter."""
    
    # CSS for a modern card-based design
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .header {{ background-color: #2c3e50; color: #ffffff; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; letter-spacing: 1px; }}
            .header p {{ margin: 10px 0 0; font-size: 14px; opacity: 0.8; }}
            .content {{ padding: 20px; }}
            .card {{ background: #ffffff; border-left: 4px solid #3498db; margin-bottom: 20px; padding: 15px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .card h2 {{ margin: 0 0 10px; font-size: 18px; color: #2c3e50; }}
            .card p {{ margin: 0 0 15px; color: #555; line-height: 1.6; font-size: 14px; }}
            .btn {{ display: inline-block; background-color: #3498db; color: #ffffff; text-decoration: none; padding: 8px 15px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
            .btn:hover {{ background-color: #2980b9; }}
            .footer {{ background-color: #ecf0f1; color: #7f8c8d; text-align: center; padding: 20px; font-size: 12px; }}
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

    for article in articles:
        html_content += f"""
                <div class="card">
                    <h2>✈️ {article.get('title', 'No Title')}</h2>
                    <p>{article.get('summary', 'No summary available.')}</p>
                    <a href="{article.get('link', '#')}" class="btn">READ FULL ARTICLE →</a>
                </div>
        """

    html_content += """
            </div>
            <div class="footer">
                <p>Automated Agent by UAVNewTech | Sent from Azores</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def send_email(html_body):
    """Sends the email using Gmail SMTP."""
    msg = MIMEMultipart()
    msg['From'] = f"UAV News Agent <{EMAIL_SENDER}>"
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = f"🚀 Weekly Drone & LiDAR Report: {datetime.now().strftime('%Y-%m-%d')}"

    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("❌ Error: Email credentials missing.")
    else:
        top_news = parse_news_file()
        if top_news:
            email_html = generate_html(top_news)
            send_email(email_html)
        else:
            print("⚠️ No news found to send.")
