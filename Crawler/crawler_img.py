import argparse
import sys
import os
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Import the AI Helmet Detector from filter.py
try:
    from filter import MotorcycleRiderDetector as Detector
except ImportError:
    Detector = None

def setup_driver():
    """Sets up a headless Chrome driver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"[!] Error setting up Chrome driver: {e}")
        return None

def extract_images(url, output_file=None, filter_helmet=False):
    """
    Navigates to a URL and extracts image resource links.
    Optionally filters for motorcycle riders in the street using AI.
    Appends unique new results to the output file.
    """
    driver = setup_driver()
    if not driver:
        print("[!] Could not initialize browser. Please ensure Chrome is installed.")
        return set()

    # Initialize AI Detector if requested
    detector = None
    if filter_helmet:
        if Detector:
            print("[*] Initializing AI Rider Detector for real-time filtering...")
            try:
                detector = Detector()
            except Exception as e:
                print(f"[!] Warning: Could not initialize AI filter: {e}. Proceeding without filtering.")
        else:
            print("[!] Warning: `filter.py` or AI dependencies missing. Proceeding without filtering.")

    print(f"[*] Navigating to: {url}")
    img_urls = set()
    
    try:
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scroll down to trigger lazy loading
        print("[*] Scrolling to capture lazy-loaded images...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3): 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract all potential image URLs
        tags = []
        tags.extend(driver.find_elements(By.TAG_NAME, "img"))
        tags.extend(driver.find_elements(By.CSS_SELECTOR, "link[rel*='icon'], link[rel*='apple-touch-icon']"))
        
        print(f"[*] Analyzing {len(tags)} potential image resources...")
        
        for tag in tags:
            try:
                src = tag.get_attribute("src") or tag.get_attribute("href")
                if src:
                    absolute_url = urljoin(url, src)
                    if absolute_url in img_urls:
                        continue

                    # AI Filtering
                    if detector:
                        if detector.is_rider(absolute_url):
                            print(f"[+] Rider identified: {absolute_url[:60]}...")
                            img_urls.add(absolute_url)
                    else:
                        img_urls.add(absolute_url)
            except:
                continue

    except Exception as e:
        print(f"[!] Error during image extraction: {e}")
    finally:
        driver.quit()

    if not img_urls:
        print("[!] No matching image URLs discovered.")
        return set()

    if output_file:
        existing_urls = set()
        if os.path.exists(output_file):
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    existing_urls = {line.strip() for line in f if line.strip()}
            except:
                pass
        
        # Only append truly new URLs
        new_urls = img_urls - existing_urls
        
        if new_urls:
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            print(f"[*] Appending {len(new_urls)} new unique image links to '{output_file}'...")
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    for img_url in sorted(new_urls):
                        f.write(img_url + "\n")
                print("[+] Done!")
            except Exception as e:
                print(f"[!] Error saving to file: {e}")
        else:
            print("[*] All found images were already in the file. Skipping append.")
    
    return img_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract image resources with optional AI filtering.")
    parser.add_argument("url", type=str, help="Target website URL")
    parser.add_argument("-o", "--output", type=str, default="url_img.txt", help="Output file")
    parser.add_argument("--filter-helmet", "--filter-rider", action="store_true", dest="filter_helmet", help="Use AI to only save images with riders/helmets")

    args = parser.parse_args()

    target_url = args.url
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    extract_images(target_url, args.output, args.filter_helmet)
