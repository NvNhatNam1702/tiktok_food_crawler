import time
from selenium.webdriver.common import service
import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_tiktok_search_urls(keyword, max_videos):
    # 1. SETUP SELENIUM (Headless usually gets blocked by TikTok, so use visible mode)
    options = Options()
    options.binary_location= "/usr/bin/chromium"
    # options.add_argument("--headless")  # Uncomment if you feel lucky
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    #set up service 
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    
    # 2. OPEN SEARCH PAGE
    search_url = f"https://www.tiktok.com/search?q={keyword}"
    print(f"Opening: {search_url}")
    driver.get(search_url)

    # 3. MANUAL CAPTCHA SOLVE (Wait for user)
    # TikTok almost always throws a captcha on search pages. 
    print("\n⚠️  PLEASE SOLVE CAPTCHA IN THE BROWSER IF IT APPEARS! ⚠️")
    print("Waiting 15 seconds...")
    time.sleep(20) 

    collected_urls = set()
    scroll_attemp = 0 
    max_scroll_attempts_without_new_data = 5
    last_count = 0 
    # 4. SCROLL AND HARVEST
    print("Scrolling to find videos...")
    while len(collected_urls) < max_videos:
        # Find video links (The selector usually points to the 'a' tag in search results)
        # Note: TikTok class names change often. Looking for links with '/video/' is safer.
        elements = driver.find_elements(By.TAG_NAME, "a")
        
        for elem in elements:
            try:
                href = elem.get_attribute('href')
                if href and "/video/" in href:
                    collected_urls.add(href)
                    if len(collected_urls) >= max_videos:
                        break
            except : 
                continue
        current_count = len(collected_urls) 
        print(f"found {current_count} unique video")
        #check if agent is stuck
        if current_count == last_count : 
            scroll_attemp +=1 
            print(f"no video founds, re_attemp: {scroll_attemp}/{max_scroll_attempts_without_new_data}")
            if scroll_attemp >= max_scroll_attempts_without_new_data: 
                print("reached end")
                break
        else :
            scroll_attemp = 0 
            last_count = current_count
        if len(collected_urls) >= max_videos : 
            break


        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    driver.quit()
    return list(collected_urls)

def download_videos(url_list):
    ydl_opts = {
        'skip_download': True,      # Subs only
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['all'],
        'outtmpl': 'search_results/%(id)s',
        'ignoreerrors': True,
        'quiet': True,
        'subtitleslangs': ['vi.*', 'vi'],
    }

    print(f"\nDownloading subtitles for {len(url_list)} videos...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url_list)

# --- EXECUTION ---
keyword = "Da Nang Food"
print(f"Searching for: {keyword}")

# Step 1: Get Links
video_links = get_tiktok_search_urls(keyword, max_videos=100)

# Step 2: Download Subs
if video_links:
    download_videos(video_links)
    print("Done!")
else:
    print("No videos found. Did Captcha block you?")
