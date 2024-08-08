from bs4 import BeautifulSoup
import os
import json

OUTPUT_PATH = "outputs"

def tags_and_attrs_remove(html_content, to_file=False):
    """Description: """
    if os.path.exists(str(html_content)):
        with open(html_content, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    else:
        soup = BeautifulSoup(html_content, "html.parser")

    target_attrs = ['class', 'style', 'id', 'viewbox', 'fill', 'stroke', 'stroke-width', 'd', 'transform', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width', 'height', 'aria-labelledby', 'aria-hidden', 'focusable', 'aria-label', 'aria-labelledby', 'aria-hidden', 'role', 'xmlns', 'width']
    target_tags = ['img', 'footer', 'svg', 'style']

    # Remove all unecessary class attributes
    for tag in soup.find_all(True):
        for target_attr in target_attrs:
            if target_attr in tag.attrs:
                del tag.attrs[target_attr]


    for tag in target_tags:
        for t in soup.find_all(tag):
            t.decompose()

    # Remove all empty tags
    for tag in soup.find_all(True):
        if not tag.contents or not tag.get_text(strip=True):
            tag.decompose()

    if to_file:
        output_path = os.path.join(OUTPUT_PATH, 'clean_html_output.txt') 
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
    return str(soup)

def load_product_links(json_path, href_path, to_file=False):
    """Description: """
    # Load JSON
    if os.path.exists(str(json_path)):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json_path

    if os.path.exists(str(href_path)):
        with open(href_path, 'r', encoding='utf-8') as f:
            links = f.readlines()
    else:
        links = href_path

    for idx, item in enumerate(data):
        item['productLink'] = "https://shopee.vn" + links[idx].strip()

    if to_file:
        with open(os.path.join(OUTPUT_PATH, 'load_links.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return data

def unwrapper(file_path, to_file=False):
    """Description: """
    # Load the HTML content
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    else:
        soup = BeautifulSoup(file_path, 'html.parser')

    # Unwrap all tags, preserving only the contents
    for tag in soup.find_all(True):
        tag.unwrap()
    if to_file:
        with open(os.path.join(OUTPUT_PATH, 'raw_output.txt'), 'w', encoding='utf-8') as file:
            file.write(str(soup))
    
    return str(soup)

def get_product_links(file_path, to_file=False):
    """Description: """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    else:
        soup = BeautifulSoup(file_path, 'html.parser')

    exceptions = ['find_similar_products', 'daily_discover', 'product_list']
    hrefs = []

    for tag in soup.find_all(href=True):
        if not any(exception in tag['href'] for exception in exceptions):
            hrefs.append(tag['href'])

    if to_file:
        with open(os.path.join(OUTPUT_PATH, 'hrefs.txt'), 'w', encoding='utf-8') as file:
            for href in hrefs:
                file.write(href + '\n')
    return hrefs

def get_actual_price(json_path, to_file=False):
    if os.path.exists(str(json_path)):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = json_path
    
    # Formula: (Discounted Price / (100 - Discount Value)) * 100 
    for item in data:
        item['actualPrice'] = int(item['discountedPrice'] / (100 - int(item['discount']))) * 100
        
    if to_file:
        with open(os.path.join(OUTPUT_PATH, 'load_price.json'), 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    return data

def get_brand_link(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    else:
        soup = BeautifulSoup(path, 'html.parser')

    for tag in soup.find_all(href=True):
        if '?brands' in tag['href']:
            if os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(tag['href'])
            return tag['href']
        
def organize_json(general_json, detailed_json, to_file=False):
    if os.path.exists(str(general_json)):
        with open(general_json, 'r', encoding='utf-8') as file:
            general_data = json.load(file)
    else:
        general_data = general_json

    if os.path.exists(str(detailed_json)):
        with open(detailed_json, 'r', encoding='utf-8') as file:
            detailed_data = json.load(file)
    else:
        detailed_data = detailed_json

    product = {
        "name": "string",
        "description": "string",
        "intendedUse": "string",
        "manufacturerName": "string",
        "manufacturerLink": "string",
        "additionalInfo": "string",
        "distributorName": "string",
        "distributorLink": "string",
        "actualPrice": 0,
        "discountedPrice": 0,
        "salesCount": 0,
        "productLink": "string"
    }

    product['name'] = general_data['name']
    product['description'] = detailed_data['description']
    product['intendedUse'] = detailed_data['intendedUse']
    product['manufacturerName'] = detailed_data['manufacturerName']
    product['manufacturerLink'] = detailed_data['manufacturerLink']
    product['additionalInfo'] = detailed_data['additionalInfo']
    product['distributorName'] = detailed_data['distributorName']
    product['distributorLink'] = detailed_data['distributorLink']
    product['actualPrice'] = general_data['actualPrice']
    product['discountedPrice'] = general_data['discountedPrice']
    product['salesCount'] = general_data['salesCount']
    product['productLink'] = general_data['productLink']

    if to_file:
        with open(os.path.join(OUTPUT_PATH, 'final_output.json'), 'w', encoding='utf-8') as file:
            json.dump(product, file, ensure_ascii=False, indent=4)
    
    return product
