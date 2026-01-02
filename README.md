# 🚁 UAVNewTech
### Automated Intelligence for Drones, LiDAR & Remote Sensing

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/Actions-Automated-green?style=for-the-badge&logo=githubactions)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)
[![Website](https://img.shields.io/badge/Live-Web_Dashboard-orange?style=for-the-badge&logo=rss)](https://filmfer.github.io/UAVNewTech/)

**UAVNewTech** is a fully automated "Free Agent" that monitors the web for the latest breakthroughs in UAVs, LiDAR, and Agricultural Remote Sensing. It runs autonomously on GitHub servers, collecting data daily and producing a professional weekly intelligence report.

---

## 🚀 Features

### 1. 🔍 Daily Intelligence Scraper
* **Automated Search:** Runs daily at **09:00 UTC** (8 AM Azores Time).
* **Deep Filtering:** Scrapes Google Custom Search for specific topics:
    * *UAV/Drone Outbreaks*
    * *LiDAR Agriculture Technology*
    * *Forest Fire Detection Drones*
* **Data Archiving:** Appends unique findings to `top_drone_remote_sensing_links.txt`.

### 2. 📧 Weekly Smart Newsletter
* **Monday Briefing:** Every Monday at **10:00 AM Azores Time**, the agent analyzes the week's findings.
* **Dynamic Design:** Generates a modern, "Canva-style" HTML newsletter.
* **Smart Icons:** Automatically assigns icons (🛰️, 🚁, 📡) based on content analysis (Satellite vs. Drone vs. Radar).
* **Delivery:** Sends a beautifully formatted email directly to your inbox.

### 3. 🌐 Live Web Dashboard
* **Instant Publishing:** The weekly report is automatically converted to a static website.
* **Always Online:** Hosted for free via GitHub Pages.
* **Live Link:** [View the Latest Report](https://filmfer.github.io/UAVNewTech/)

---

## ⚙️ Architecture

The project consists of three autonomous agents:

| Agent | File | Schedule | Function |
| :--- | :--- | :--- | :--- |
| **The Collector** | `scraper.py` | Daily | Searches the web, filters "last month" results, and saves unique links. |
| **The Publisher** | `newsletter.py` | Mondays | Reads collected links, generates HTML, sends email, and deploys to Web. |
| **The Janitor** | `cleanup.py` | Monthly | Automatically deletes links older than 90 days to maintain database health. |

---

## 🛠️ Setup & Deployment

### Prerequisites
* Python 3.10+
* A Google Cloud Project (for Search API)
* A Gmail Account (for sending newsletters)

### 🔐 Configuration (GitHub Secrets)
To deploy this yourself, add the following **Secrets** to your repository settings:

| Secret Name | Description |
| :--- | :--- |
| `GOOGLE_API_KEY` | Your Google Cloud API Key (Enabled for Custom Search). |
| `CUSTOM_SEARCH_ENGINE_ID` | Your Programmable Search Engine ID (CX). |
| `EMAIL_USER` | The Gmail address that sends the report. |
| `EMAIL_PASSWORD` | The **App Password** for that Gmail account (Not your login password). |

### 📦 Installation
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/filmfer/UAVNewTech.git](https://github.com/filmfer/UAVNewTech.git)
    ```
2.  **Enable GitHub Pages:**
    * Go to *Settings* > *Pages*.
    * Set Source to **GitHub Actions**.
3.  **Run Manually:**
    * Go to the *Actions* tab and run the **"Daily Drone Scrape"** or **"Weekly Newsletter"** workflow.

---

## 📂 Output Files
* 📄 **[top_drone_remote_sensing_links.txt](top_drone_remote_sensing_links.txt):** The raw database of collected articles.
* 🌐 **[index.html](index.html):** The source code for the live dashboard.
* 📝 **scraper.log:** Execution logs (available in Artifacts).

---

## 📬 Contact

**Project Maintainer:** filmfer
📧 **Email:** [filmfer@gmail.com](mailto:filmfer@gmail.com)

*Feel free to open an issue or pull request if you have ideas for new data sources!*

---
© 2026 UAVNewTech. Open Source under [MIT License](LICENSE).
