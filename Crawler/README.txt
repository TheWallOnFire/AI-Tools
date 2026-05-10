=========================================================
AI IMAGE CRAWLER & ANNOTATOR - COMMAND GUIDE
=========================================================

This project is a complete pipeline for searching the web, 
downloading images, filtering them for specific content (riders/street), 
and generating COCO-format annotations for AI training.

---------------------------------------------------------
1. CRAWLING (Searching for Images)
---------------------------------------------------------
Use 'main.py' to search the web and extract image URLs.

Usage:
  python main.py "your keyword" [site_count]

Flags:
  --filter-rider  : Use AI to only save images of people on motorcycles in the street.
  --filter-helmet : (Alias) same as --filter-rider.
  -o [filename]   : Change the output text file (default: url_img.txt).

Example:
  python main.py "people riding motorbikes city street" 10 --filter-rider

---------------------------------------------------------
2. DOWNLOADING IMAGES
---------------------------------------------------------
Use 'download.py' to download all URLs saved in 'url_img.txt'.

Usage:
  python download.py

* Images are saved to: data/raw/crawl/

---------------------------------------------------------
3. GENERATING ANNOTATIONS (COCO Format)
---------------------------------------------------------
Use 'annotation.py' to create JSON annotations for your images.

Usage (Basic - Full image boxes):
  python annotation.py

Usage (AI-Powered - Precise Bounding Boxes):
  python annotation.py --detect

Options:
  --category [name]  : Name for the detected object (default: motorcycle_rider).
  --threshold [0-1]  : Set AI confidence (default: 0.1).
  --limit [N]        : Only process first N images (useful for testing).
  --no-fallback      : Don't create boxes for images where AI finds nothing.
  --output [path]    : Save to a custom JSON file.

Example (AI Detection on 5 images):
  python annotation.py --detect --limit 5 --category "motorcycle_rider"

---------------------------------------------------------
4. VIEWING THE GALLERY
---------------------------------------------------------
Use 'gallery_app.py' to view your collected images in a web browser.

Usage:
  streamlit run gallery_app.py

---------------------------------------------------------
WORKFLOW SUMMARY:
1. python main.py "people riding motorbikes city street" 10 --filter-rider
2. python download.py
3. python annotation.py --detect
4. streamlit run gallery_app.py
=========================================================
