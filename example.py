from bs4 import BeautifulSoup
from shopee_crawler.pipeline import ProductListCrawler, DetailedInfoCrawler
from shopee_crawler.functions import organize_json

# Specify html file path
HTML_PATH = 'homepage.html'

# Load HTML file
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Get daily suggestion chunk
daily_suggestion_html = soup.find("div", class_="stardust-tabs-panels")

# Get product list
product_list = ProductListCrawler(daily_suggestion_html)

# Get detailed product information (detailed html page must be manually saved)
product_details = DetailedInfoCrawler('output.html')

# Get full product detail by merging product list and product details into 1 JSON object
full_product_detail_sample = organize_json(general_json=product_list[0], detailed_json=product_details, to_file=True)

print(full_product_detail_sample)