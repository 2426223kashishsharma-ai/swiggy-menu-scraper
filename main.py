import json
import os
import sys

# Ensure local imports work cleanly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import RestaurantData
from parser import parse_swiggy_html
from scraper import fetch_swiggy_html


def run_batch_scraper():
    # 1. Load URLs from restaurants.txt
    urls_file = "restaurants.txt"

    if not os.path.exists(urls_file):
        print(
            f"Error: '{urls_file}' not found. Creating a default file with test URL..."
        )
        with open(urls_file, "w") as f:
            f.write(
                "https://www.swiggy.com/city/ahmedabad/mcdonalds-satellite-rest123456\n"
            )

    with open(urls_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Found {len(urls)} URL(s) to process.")

    # 2. Output directory setup
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    all_results = []

    # 3. Scrape each URL
    for idx, url in enumerate(urls, 1):
        print(f"\n[{idx}/{len(urls)}] Processing: {url}")
        try:
            html = fetch_swiggy_html(url)
            data: RestaurantData = parse_swiggy_html(html, url)

            all_results.append(data.model_dump())
            print(
                f"Successfully scraped: {data.restaurant_name} ({data.total_items} items)"
            )

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    # 4. Save aggregated output to JSON
    output_file = os.path.join(output_dir, "scraped_restaurants.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\nScraping finished! Output saved to: {output_file}")


if __name__ == "__main__":
    run_batch_scraper() 
