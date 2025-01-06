# Tiktok_Osint_Scraper_With_Python
TikTok Profile Scraper: A Python tool that scrapes public TikTok profiles, extracting details such as nickname, bio, followers, following, profile picture, and the first 5 video stats. Utilizes Selenium for web automation and scraping.


README.md Template:
markdown
Copy code
# TikTok Profile Scraper

**TikTok Profile Scraper** is a Python tool that allows you to extract public profile data from TikTok, including:
- Nickname
- Bio
- Followers, Following, Likes
- Profile Picture URL
- First 5 video statistics (Likes, Comments, Shares, Description)

The tool uses **Selenium** and **Chrome WebDriver** to scrape profile data.

## Features:
- Scrape TikTok profiles based on usernames.
- Save the extracted data as JSON files.
- Headless operation for background running.

## Requirements:
- Python 3.x
- Google Chrome
- ChromeDriver (automatically managed with `webdriver-manager`)
- `selenium` Python package

## Setup & Installation:

### 1. Clone the Repository
```bash
git clone https://github.com/username/repository-name.git
cd repository-name
2. Set up a Virtual Environment (Optional but Recommended)
It’s recommended to create a virtual environment to avoid conflicts with other Python packages:

bash
Copy code
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3. Install Dependencies
Once your virtual environment is active, install the required packages:

bash
Copy code
pip install -r requirements.txt
If requirements.txt does not exist, you can manually install the required libraries:

bash
Copy code
pip install selenium webdriver-manager
4. Running the Script
To scrape a TikTok profile, simply run the script:

bash
Copy code
python main.py
It will prompt you to enter a TikTok username to scrape. The script will extract the profile data and save it to a JSON file.
