import argparse
import sys
import os
from crawler_web import crawl_with_selenium as get_website_urls
from crawler_img import extract_images as get_image_urls

# History Tracking Configuration
HISTORY_FILE = "crawled_sites.txt"

def load_history():
    """Returns a set of URLs that have already been processed."""
    if not os.path.exists(HISTORY_FILE):
        return set()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except Exception as e:
        print(f"[!] Warning: Could not load history file: {e}")
        return set()

def save_to_history(url):
    """Appends a single URL to the history file."""
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(url + "\n")
    except Exception as e:
        print(f"[!] Warning: Could not save to history: {e}")

def orchestrate_crawl(keyword, website_count, output_file, filter_helmet=False):
    """
    Orchestrates the workflow:
    1. Find website URLs based on a keyword.
    2. Skip URLs that have been processed in previous runs.
    3. For each new site, extract relevant image URLs.
    4. Append new image URLs to the global output file.
    """
    print(f"[*] Starting Persistent Crawler Workflow...")
    print(f"[*] Keyword: {keyword}")
    print(f"[*] Target Website Count: {website_count}")
    print(f"[*] AI Rider/Street Filtering: {'Enabled' if filter_helmet else 'Disabled'}")
    
    # Load history
    history = load_history()
    if history:
        print(f"[*] Loaded history: {len(history)} sites previously crawled.")
    
    # Step 1: Get website URLs from search engines
    found_sites = get_website_urls(keyword, website_count, engine='ddg')
    
    if not found_sites:
        print("[!] No websites found for the given keyword. Aborting.")
        return

    # Filter out sites we've already handled
    new_sites = [s for s in found_sites if s not in history]
    skipped_count = len(found_sites) - len(new_sites)
    
    if skipped_count > 0:
        print(f"[*] Skipping {skipped_count} sites already found in history.")

    if not new_sites:
        print("[!] No new sites to process. Try a different keyword or increase count.")
        return

    print(f"\n[*] Processing {len(new_sites)} new websites...")
    total_images_added = 0
    
    # Step 2: Extract images from each new site
    for i, site in enumerate(new_sites, 1):
        print(f"\n[{i}/{len(new_sites)}] Processing: {site}")
        try:
            # crawler_img.py already handles append logic internally
            site_images = get_image_urls(site, output_file=output_file, filter_helmet=filter_helmet)
            
            if site_images:
                print(f"[+] Processed site. Moving to history.")
                total_images_added += len(site_images)
            else:
                print("[-] No images found. Moving to history anyway.")
            
            # Record success in history
            save_to_history(site)
            
        except Exception as e:
            print(f"[!] Unexpected error processing site {site}: {e}")

    print(f"\n[✓] Workflow Complete.")
    print(f"[*] Successfully processed {len(new_sites)} new websites.")
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                total_total = len(f.readlines())
            print(f"[*] Total cumulative images in '{output_file}': {total_total}")
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrate persistent, cumulative web search and image extraction.")
    parser.add_argument("keyword", type=str, help="Keyword for web search")
    parser.add_argument("count", type=int, help="Number of websites to crawl")
    parser.add_argument("-o", "--output", type=str, default="url_img.txt", help="Output file")
    parser.add_argument("--filter-helmet", "--filter-rider", action="store_true", dest="filter_helmet", help="Use AI to only save images with riders/helmets")

    args = parser.parse_args()

    orchestrate_crawl(args.keyword, args.count, args.output, args.filter_helmet)
