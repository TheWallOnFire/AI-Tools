import os
import requests
import base64
import time
from io import BytesIO
from PIL import Image
from tqdm import tqdm

# Configuration
INPUT_FILE = "url_img.txt"
OUTPUT_DIR = "data/raw/crawl/"

def ensure_dir(directory):
    """Creates the directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"[*] Created output directory: {directory}")

def download_images():
    """Reads URLs from file and downloads them as PNG files."""
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Input file `{INPUT_FILE}` not found.")
        return

    # Create output directory
    ensure_dir(OUTPUT_DIR)

    # Load URLs
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("[!] No URLs found to download.")
        return

    print(f"[*] Starting download of {len(urls)} images...")
    success_count = 0
    fail_count = 0

    # Progress bar
    for count, url in enumerate(tqdm(urls, desc="Downloading"), 1):
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"pic{count}_{timestamp}_{count}.png"  # Added count at end to ensure uniqueness within same second
            filepath = os.path.join(OUTPUT_DIR, filename)

            img = None
            if url.startswith("data:image"):
                # Handle Base64
                header, encoded = url.split(",", 1)
                image_data = base64.b64decode(encoded)
                img = Image.open(BytesIO(image_data))
            else:
                # Handle HTTP/HTTPS
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                else:
                    fail_count += 1
                    continue

            if img:
                # Convert to RGB (required for saving some formats to PNG if they have alpha or are CMYK/Grayscale)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Save as PNG
                img.save(filepath, "PNG")
                success_count += 1

        except Exception as e:
            # print(f"Error downloading {url[:50]}... : {e}")
            fail_count += 1
            continue

    print(f"\n[✓] Download Process Complete.")
    print(f"[+] Successfully downloaded: {success_count} images")
    print(f"[-] Failed: {fail_count} images")
    print(f"[*] All files are saved in: `{OUTPUT_DIR}`")

if __name__ == "__main__":
    download_images()
