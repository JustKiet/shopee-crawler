from shopee_crawler.functions import tags_and_attrs_remove, load_product_links, unwrapper, get_product_links, get_brand_link, get_actual_price
from shopee_crawler.llm_processing import llm_jsonify, llm_distributor_identifier, llm_get_product_detail
from bs4 import BeautifulSoup
import os
import json

OUTPUT_PATH = "outputs"

def ProductListCrawler(html_path, to_file=False):
    """Description: """
    
    if os.path.exists(str(html_path)):
        with open(html_path, "r", encoding="utf-8") as file:
            html = file.read()
    else:
        html = str(html_path)

    html_cleaned = tags_and_attrs_remove(html, to_file=False)

    html_unwrapped = unwrapper(html_cleaned)

    hrefs = get_product_links(html_cleaned)

    json_output = llm_jsonify(html_unwrapped)

    with_price = get_actual_price(json_output)

    output = load_product_links(with_price, hrefs)

    if to_file:
        with open(os.path.join(OUTPUT_PATH, "product_list_output.json"), "w", encoding="utf-8") as file:
            json.dump(output, file, ensure_ascii=False, indent=4)

    return output

def DetailedInfoCrawler(html_path, to_file=False):
    """Description: """
    
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    else:
        soup = BeautifulSoup(html_path, "html.parser")

    distributor_detail_section = soup.find("section", class_="page-product__shop")
    product_detail_section = soup.find("div", class_="product-detail page-product__detail")

    # Get distributor name and link
    distributor_raw_content = tags_and_attrs_remove(str(distributor_detail_section))
    distributor_link = get_product_links(distributor_raw_content)
    distributor_detail_unwrapped = unwrapper(distributor_raw_content)
    distributor_name = llm_distributor_identifier(distributor_detail_unwrapped)

    # Get product details
    manufacturer_raw_content = tags_and_attrs_remove(str(product_detail_section))
    manufacturer_link = get_brand_link(manufacturer_raw_content)
    product_detail_unwrapped = unwrapper(manufacturer_raw_content)
    product_detail_json = llm_get_product_detail(product_detail_unwrapped)

    # Merge to output JSON
    output_json = product_detail_json
    output_json['distributorLink'] = "https://shopee.vn" + str(distributor_link[0]).strip()
    output_json['distributorName'] = distributor_name
    output_json['manufacturerLink'] = manufacturer_link

    if to_file:
        with open(os.path.join(OUTPUT_PATH, "detailed_info_output.json"), "w", encoding="utf-8") as file:
            json.dump(output_json, file, ensure_ascii=False, indent=4)

    return output_json

