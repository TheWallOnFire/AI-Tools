import requests
import base64
import torch
import os
from io import BytesIO
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class MotorcycleRiderDetector:
    """
    AI-powered detector to identify people on motorbikes in the street.
    Uses CLIP (Zero-shot classification) for inference.
    """
    def __init__(self, threshold=0.65, model_id="openai/clip-vit-base-patch32"):
        """Initializes the CLIP model and processor."""
        self.threshold = threshold
        self.labels = ["a photo of a person riding a motorbike on the street", "an image without a person riding a motorbike"]
        
        # Load model and processor once to save resources
        # print(f"[*] Initializing AI Helmet Detector (Model: {model_id})...")
        try:
            self.model = CLIPModel.from_pretrained(model_id)
            self.processor = CLIPProcessor.from_pretrained(model_id)
        except Exception as e:
            # print(f"[!] Error loading AI model: {e}")
            raise RuntimeError(f"Failed to load AI model: {e}")

    def load_image(self, url):
        """Loads and decodes an image from a URL or Base64 data string."""
        try:
            if url.startswith("data:image"):
                header, encoded = url.split(",", 1)
                image_data = base64.b64decode(encoded)
                return Image.open(BytesIO(image_data)).convert("RGB")
            else:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return Image.open(BytesIO(response.content)).convert("RGB")
        except:
            pass
        return None

    def is_rider(self, url):
        """Returns True if the image likely contains a person riding a motorbike on the street."""
        img = self.load_image(url)
        if img is None:
            return False

        try:
            # Preprocess and Run CLIP
            inputs = self.processor(text=self.labels, images=img, return_tensors="pt", padding=True)
            outputs = self.model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)
            
            # Label index 0 = "person riding a motorbike on the street"
            rider_score = probs[0][0].item()
            return rider_score >= self.threshold
        except:
            return False

# Standalone execution for compatibility with old workflow
if __name__ == "__main__":
    import argparse
    from tqdm import tqdm

    def run_standalone():
        input_file = "url_img.txt"
        output_file = "url_helmet.txt"
        
        if not os.path.exists(input_file):
            print(f"[!] Input file `{input_file}` not found.")
            return

        with open(input_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]

        print(f"[*] Analyzing {len(urls)} images for riders...")
        detector = MotorcycleRiderDetector()
        
        rider_urls = []
        for url in tqdm(urls, desc="Filtering Riders"):
            if detector.is_rider(url):
                rider_urls.append(url)

        with open(output_file, "w", encoding="utf-8") as f:
            for url in rider_urls:
                f.write(url + "\n")
        print(f"[OK] Saved {len(rider_urls)} matches to {output_file}")

    run_standalone()
