import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def configure_driver():
    """Sets up the Selenium WebDriver with Chrome."""
    chrome_options = Options()
    # Disabled headless mode for debugging (comment out headless line)
    # chrome_options.add_argument("--headless")  # Headless mode disabled for debugging
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")  # Maximize window
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable WebGL
    chrome_options.add_argument("--disable-hardware-acceleration")  # Disable GPU hardware acceleration
    # Add user-agent to avoid bot blocking
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def fetch_profile_data(driver, username):
    """Fetch public profile data from TikTok."""
    print(f"[INFO] Scraping TikTok profile: {username}")
    url = f"https://www.tiktok.com/@{username}"
    driver.get(url)

    try:
        # Increased wait time to account for dynamic page loading (30 seconds)
        wait = WebDriverWait(driver, 30)

        # Wait for nickname (Display Name)
        print("[INFO] Waiting for nickname...")
        nickname = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'share-title')]"))
        ).text
        print(f"[INFO] Nickname found: {nickname}")

        # Wait for bio (if available)
        print("[INFO] Waiting for bio...")
        try:
            bio = driver.find_element(By.XPATH, "//div[contains(@data-e2e, 'user-bio')]").text
        except Exception:
            bio = "No bio available."
        print(f"[INFO] Bio: {bio}")

        # Wait for profile statistics (followers, following, likes)
        print("[INFO] Waiting for stats (followers, following, likes)...")
        stats = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//strong[contains(@data-e2e, 'stat-number')]"))
        )
        followers = stats[0].text if len(stats) > 0 else "0"
        following = stats[1].text if len(stats) > 1 else "0"
        likes = stats[2].text if len(stats) > 2 else "0"
        print(f"[INFO] Followers: {followers}, Following: {following}, Likes: {likes}")

        # Wait for profile picture URL
        print("[INFO] Waiting for profile picture...")
        profile_pic = driver.find_element(By.XPATH, "//img[contains(@class, 'tiktok-avatar')]").get_attribute("src")

        # Collect video data (limited to 5 for now)
        print("[INFO] Collecting video data...")
        videos = driver.find_elements(By.XPATH, "//div[@data-e2e='user-post-item']")
        video_data = []
        for video in videos[:5]:  # Limit to first 5 videos
            try:
                description = video.find_element(By.XPATH, ".//p[contains(@class, 'tiktok-video-desc')]").text
                stats = video.find_elements(By.XPATH,
                                            ".//span[contains(@class, 'like') or contains(@class, 'comment') or contains(@class, 'share')]")

                # Extract stats from the video (likes, comments, shares)
                likes = stats[0].text if len(stats) > 0 else "0"
                comments = stats[1].text if len(stats) > 1 else "0"
                shares = stats[2].text if len(stats) > 2 else "0"

                video_data.append({
                    "description": description,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                })
            except Exception as e:
                print(f"[ERROR] Failed to scrape video stats: {e}")

        # Build the profile data dictionary
        profile_data = {
            "username": username,
            "nickname": nickname,
            "bio": bio,
            "followers": followers,
            "following": following,
            "likes": likes,
            "profile_picture": profile_pic,
            "videos": video_data,
        }
        return profile_data

    except Exception as e:
        print(f"[ERROR] Failed to scrape profile: {e}")
        return None


def save_to_file(username, data):
    """Save extracted profile data to a JSON file."""
    filename = f"{username}_profile.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[INFO] Profile data saved to {filename}")


def main():
    # Set up the WebDriver
    driver = configure_driver()

    try:
        target_username = input("Enter TikTok Username to scrape: ").strip()
        profile_data = fetch_profile_data(driver, target_username)

        if profile_data:
            print("\n[INFO] Profile Data Extracted:")
            for key, value in profile_data.items():
                print(f"{key}: {value}")
            save_to_file(target_username, profile_data)
        else:
            print("[ERROR] Failed to extract profile data.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
