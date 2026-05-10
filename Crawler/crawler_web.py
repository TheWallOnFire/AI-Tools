import argparse
import sys
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

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
        print("[*] Attempting fallback to direct browser initialization...")
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e2:
            print(f"[!] Fallback failed: {e2}")
            return None

def extract_links(driver, engine, urls, count):
    """Extracts organic links from the current page state."""
    if engine == 'ddg':
        # DuckDuckGo links are usually in article h2 a or .result__a
        selectors = ["article h2 a", ".result__a", "[data-testid='result-title-a']"]
    else: # bing
        selectors = ["h2 a", ".b_algo h2 a"]

    found_in_round = 0
    for selector in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for elem in elements:
            try:
                href = elem.get_attribute("href")
                if href and href.startswith("http") and not any(x in href for x in ["duckduckgo.com", "bing.com", "microsoft.com"]):
                    if href not in urls:
                        urls.add(href)
                        found_in_round += 1
                        if len(urls) >= count:
                            return found_in_round
            except:
                continue
    return found_in_round

def crawl_with_selenium(keyword, count, engine='ddg'):
    """Crawls URLs using Selenium with support for high-volume collection (up to count)."""
    driver = setup_driver()
    if not driver:
        print("[!] Could not initialize browser. Please ensure Chrome is installed.")
        return []

    urls = set() # Use a set for automatic deduplication
    print(f"[*] Starting crawl for: '{keyword}' (Target: {count})")
    print(f"[*] Engine: {engine}")

    try:
        if engine == 'ddg':
            search_url = f"https://duckduckgo.com/?q={keyword}"
            driver.get(search_url)
            
            # Initial wait
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article, .result__a"))
            )

            last_len = 0
            no_new_results_count = 0
            
            while len(urls) < count:
                # Extract currently visible links
                extract_links(driver, engine, urls, count)
                
                new_total = len(urls)
                if new_total > last_len:
                    print(f"[+] Progress: {new_total}/{count} URLs collected...")
                    last_len = new_total
                    no_new_results_count = 0
                else:
                    no_new_results_count += 1
                
                if no_new_results_count > 10: # If we haven't found new links in 10 scrolls, we're likely at the end
                    print("[*] No more results found after multiple scrolls. Ending crawl.")
                    break

                # Scroll to bottom to trigger infinite load
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Randomized pause to mimic human behavior and allow loading
                time.sleep(random.uniform(1.5, 3.0))
                
                # Check for "More Results" button (sometimes shows up on DDG)
                try:
                    more_results_btn = driver.find_elements(By.ID, "more-results")
                    if more_results_btn and more_results_btn[0].is_displayed():
                        more_results_btn[0].click()
                        time.sleep(2)
                except:
                    pass

        elif engine == 'bing':
            search_url = f"https://www.bing.com/search?q={keyword}"
            driver.get(search_url)
            
            while len(urls) < count:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h2 a"))
                )
                
                extract_links(driver, engine, urls, count)
                print(f"[+] Progress: {len(urls)}/{count} URLs collected...")
                
                if len(urls) >= count:
                    break
                
                # Bing pagination (Next button)
                try:
                    next_btn = driver.find_elements(By.CSS_SELECTOR, "a[title='Next page'], .sb_pagN")
                    if next_btn:
                        next_btn[0].click()
                        time.sleep(random.uniform(2, 4))
                    else:
                        print("[*] No 'Next' button found. Ending crawl.")
                        break
                except Exception as e:
                    print(f"[*] Pagination error or end of results: {e}")
                    break

    except Exception as e:
        print(f"[!] Selenium crawl error: {e}")
    finally:
        driver.quit()
    
    return list(urls)

def save_urls(urls, output_file):
    if not urls:
        print("[!] No URLs discovered.")
        return

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    print(f"[*] Finalizing: Saving {len(urls)} unique URLs to '{output_file}'...")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        print("[+] Done!")
    except Exception as e:
        print(f"[!] Error saving to file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="High-Volume Selenium-based URL Crawler.")
    parser.add_argument("keyword", type=str, help="Search keyword")
    parser.add_argument("count", type=int, help="Number of URLs to fetch")
    parser.add_argument("-o", "--output", type=str, default="url_link.txt", help="Output file (default: url_link.txt)")
    parser.add_argument("-e", "--engine", type=str, choices=['ddg', 'bing'], default='ddg', help="Engine (default: ddg)")

    args = parser.parse_args()

    # Cap the count to something reasonable if it's too high, or just let it go
    # The user asked for under 10000, so we'll respect that.
    results = crawl_with_selenium(args.keyword, args.count, args.engine)
    save_urls(results, args.output)
