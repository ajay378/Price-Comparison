import json
import re
import csv
from bs4 import BeautifulSoup
import requests  # For live fetching

# Primary: Fetch LIVE complete HTML from Buyhatke
url = 'https://buyhatke.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
try:
    print("Fetching live HTML from Buyhatke...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    html_content = response.text
    # SAVE FULL HTML TO FILE for offline use/verification
    with open('homepage.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"SUCCESS: Fetched and saved full HTML to homepage.html. Length: {len(html_content)} chars")
    print(f"Contains 'iPhone 15'? {'iPhone 15' in html_content}")
    print(f"Contains 'serviceWorker'? {'serviceWorker' in html_content}")
    print(f"Contains 'trendingProducts'? {'trendingProducts' in html_content}")  # Key data check
except requests.RequestException as e:
    print(f"Live fetch failed: {e}. Falling back to local file 'homepage.html'.")
    try:
        with open('homepage.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"Fallback: Loaded file. Length: {len(html_content)} chars")
    except FileNotFoundError:
        raise ValueError("No 'homepage.html' file found. Run live fetch first or create it manually.")
    except Exception as file_e:
        raise ValueError(f"File loading failed: {file_e}")

def parse_buyhatke_html(html_str):
    """
    Parse the Buyhatke HTML and extract embedded JSON data.
    Dynamically finds SvelteKit script (handles changing hashes).
    Returns a dictionary with key sections like trendingProducts, etc.
    """
    soup = BeautifulSoup(html_str, 'lxml')
    
    # Find ALL script tags for debug
    all_scripts = soup.find_all('script')
    print("DEBUG: Found {} script tags in total.".format(len(all_scripts)))
    
    # DYNAMIC FINDER: Look for SvelteKit script by patterns (not hardcoded ID)
    # Patterns: Contains 'sveltekit', 'kit.start', 'node_ids', and 'data: ['
    script_tag = None
    for script in all_scripts:
        script_text = script.string or ''
        if script_text and re.search(r'sveltekit.*kit\.start.*node_ids.*data:\s*\[', script_text, re.DOTALL | re.IGNORECASE):
            script_tag = script
            print("DEBUG: Found SvelteKit script (dynamic match). Length:", len(script_text))
            break
    
    if not script_tag:
        print("DEBUG: No exact SvelteKit script found. Falling back to text search for data patterns.")
        script_content = html_str  # Use full HTML for fallback extraction
    else:
        script_content = script_tag.string
        print("DEBUG: First 500 chars of script:")
        print(script_content[:500])
        print("-" * 50)
    
    # IMPROVED REGEX: Capture the FULL data array (greedy, handles dynamic structure)
    # Look for 'data: [' ... '], form:' or end of object
    data_match = re.search(r'data:\s*(\[[\s\S]*?)\]\s*,\s*form:', script_content, re.DOTALL)
    
    if not data_match:
        # Alternative: To end of kit.start object
        data_match = re.search(r'data:\s*(\[[\s\S]*?)\]\s*(?=\s*form|\s*\};|\s*\)\);)', script_content, re.DOTALL)
    
    if not data_match:
        # Last resort: Largest array starting with 'data: ['
        data_match = re.search(r'data:\s*(\[[\s\S]{1000,}\])', script_content, re.DOTALL)  # Min 1000 chars for full data
    
    if not data_match:
        print("DEBUG: No full data array found via regex. Using text-based fallback extraction.")
        return extract_from_text_fallback(script_content)  # See fallback function below
    
    data_str = data_match.group(1).strip()
    print("DEBUG: Captured data string length:", len(data_str))  # Should be 5000+
    print("DEBUG: First 300 chars of data:", repr(data_str[:300]))
    print("DEBUG: Last 200 chars of data:", repr(data_str[-200:]))
    
    try:
        # ENHANCED CLEANING: Convert JS to valid JSON (improved for delimiter issues)
        # 1. Quote unquoted keys (e.g., type: -> "type":)
        data_str = re.sub(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', r'"\1":', data_str)
        # 2. Quote unquoted string values (e.g., : Flipkart -> : "Flipkart")
        data_str = re.sub(r':\s*([a-zA-Z_$][a-zA-Z0-9_$]*)(?=\s*[,}\]]|$)', r': "\1"', data_str)
        # 3. Remove trailing commas more aggressively
        data_str = re.sub(r',\s*([}\]])', r'\1', data_str)
        data_str = re.sub(r',\s*(?=[}\]])', '', data_str)  # Remove lone commas before close
        # 4. Fix booleans/null (keep as is for JSON)
        data_str = data_str.replace('true', 'true').replace('false', 'false').replace('null', 'null')
        # 5. Clean newlines/escapes and fix delimiters
        data_str = re.sub(r'\\n|\\t', ' ', data_str)
        data_str = re.sub(r'\s*,\s*,\s*', ',', data_str)  # Fix double commas
        
        # Ensure array format
        if not data_str.startswith('['):
            data_str = '[' + data_str + ']'
        data_str = data_str.rstrip(',')  # Final trim
        
        parsed_data = json.loads(data_str)
        print("DEBUG: Successfully parsed FULL data array. Number of items:", len(parsed_data))
        
        # Extract key sections (main data at index 2 or scan all)
        extracted = {}
        for item in parsed_data:
            if isinstance(item, dict) and 'data' in item:
                sub_data = item['data']
                if isinstance(sub_data, dict):
                    for key in ['trendingProducts', 'exclusiveDealsProducts', 'features', 'supportedStoresFeatureInfo', 'referral']:
                        if key in sub_data:
                            extracted[key] = sub_data[key]
        
        if extracted:
            print("DEBUG: Full extraction successful. Keys found:", list(extracted.keys()))
            return extracted
        
        raise ValueError("No key sections found in parsed data.")
    
    except json.JSONDecodeError as e:
        print(f"Full JSON parsing error: {e}")
        print("DEBUG: Using text-based fallback extraction...")
        return extract_from_text_fallback(script_content)

def extract_from_text_fallback(text_content):
    """
    Fallback: Extract data directly from HTML text using regex (no BeautifulSoup needed).
    Pulls all products/deals even if script tag is missed.
    """
    extracted = {
        'trendingProducts': [],
        'exclusiveDealsProducts': [],
        'features': {}
    }
    
    # Extract trendingProducts (full pattern for all fields)
    trending_pattern = r'name\s*:\s*"([^"]*)"\s*,\s*image\s*:\s*"([^"]*)"\s*,\s*link\s*:\s*"([^"]*)"\s*,\s*cur_price\s*:\s*(\d+)\s*,\s*last_price\s*:\s*(\d+)\s*,\s*price_drop_per\s*:\s*(\d+)\s*,\s*date\s*:\s*"([^"]*)"\s*,\s*site_name\s*:\s*"([^"]*)"\s*,\s*site_logo\s*:\s*"([^"]*)"\s*,\s*site_pos\s*:\s*(\d+)\s*,\s*internalPid\s*:\s*(\d+)\s*,\s*rating\s*:\s*([\d.]+)\s*,\s*ratingCount\s*:\s*(\d+)'
    trending_matches = re.findall(trending_pattern, text_content, re.DOTALL | re.MULTILINE)
    
    for match in trending_matches:
        product = {
            'name': match[0],
            'image': match[1],
            'link': match[2],
            'cur_price': int(match[3]),
            'last_price': int(match[4]),
            'price_drop_per': int(match[5]),
            'date': match[6],
            'site_name': match[7],
            'site_logo': match[8],
            'site_pos': int(match[9]),
            'internalPid': int(match[10]),
            'rating': float(match[11]),
            'ratingCount': int(match[12])
        }
        extracted['trendingProducts'].append(product)
    
    # IMPROVED FALLBACK for exclusiveDealsProducts (tweaked regex for live structure, includes optional fields)
    deals_pattern = r'name\s*:\s*"([^"]*)"\s*,\s*(?:image\s*:\s*"([^"]*)"\s*,\s*)?(?:link\s*:\s*"([^"]*)"\s*,\s*)?cur_price\s*:\s*(\d+)\s*,\s*last_price\s*:\s*(\d+)\s*,\s*price_drop_per\s*:\s*(\d+)\s*,\s*(?:date\s*:\s*"([^"]*)"\s*,\s*)?site_name\s*:\s*"([^"]*)"\s*,\s*(?:site_logo\s*:\s*"([^"]*)"\s*,\s*)?(?:site_pos\s*:\s*(\d+)\s*,\s*)?internalPid\s*:\s*(\d+)\s*,\s*(?:rating\s*:\s*(-?\d+)\s*,\s*)?ratingCount\s*:\s*(\d+)\s*,\s*score\s*:\s*(\d+)'
    deals_matches = re.findall(deals_pattern, text_content, re.DOTALL | re.MULTILINE)
    
    for match in deals_matches:
        deal = {
            'name': match[0],
            'image': match[1] if len(match) > 1 and match[1] else None,
            'link': match[2] if len(match) > 2 and match[2] else None,
            'cur_price': int(match[3]),
            'last_price': int(match[4]),
            'price_drop_per': int(match[5]),
            'date': match[6] if len(match) > 6 and match[6] else None,
            'site_name': match[7],
            'site_logo': match[8] if len(match) > 8 and match[8] else None,
            'site_pos': int(match[9]) if len(match) > 9 and match[9] else None,
            'internalPid': int(match[10]),
            'rating': int(match[11]) if len(match) > 11 and match[11] and match[11] != '-1' else None,
            'ratingCount': int(match[12]),
            'score': int(match[13])
        }
        extracted['exclusiveDealsProducts'].append(deal)
    
    # Extract features (key-value pairs like spendButtonClicked: 218)
    features_pattern = r'([a-zA-Z]+(?:[A-Z][a-zA-Z]*)*)\s*:\s*(\d+)'
    features_matches = re.findall(features_pattern, text_content, re.MULTILINE)
    for key, value in features_matches:
        if key in ['spendButtonClicked', 'GraphClicked', 'AutoCouponClicked', 'DittoOpened', 'WatchPriceClicked', 'CompareBarNewHovered']:  # Known keys
            extracted['features'][key] = int(value)
    
    print(f"DEBUG: Fallback extracted {len(extracted['trendingProducts'])} products, {len(extracted['exclusiveDealsProducts'])} deals, and {len(extracted['features'])} features.")
    return extracted

# Run the parser
if __name__ == "__main__":
    try:
        extracted_data = parse_buyhatke_html(html_content)
        
        # Save full extracted data to JSON
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=4, ensure_ascii=False)
        print("SUCCESS: Full data saved to output.json")
        
        # Print summary
        print("\n=== EXTRACTED DATA SUMMARY ===")
        print(json.dumps(extracted_data, indent=2, ensure_ascii=False))
        
        # Print trending products
        if 'trendingProducts' in extracted_data and extracted_data['trendingProducts']:
            print("\n=== TRENDING PRODUCTS (Full List) ===")
            for i, product in enumerate(extracted_data['trendingProducts'], 1):
                print(f"{i}. {product.get('name', 'N/A')} | Price: ₹{product.get('cur_price', 'N/A')} (was ₹{product.get('last_price', 'N/A')}, {product.get('price_drop_per', 0)}% drop)")
                print(f"   Site: {product.get('site_name', 'N/A')} | Rating: {product.get('rating', 'N/A')} ({product.get('ratingCount', 0)} reviews)")
                print(f"   Link: {product.get('link', 'N/A')[:60]}...")
                if i >= 8:  # Limit to 8 for brevity
                    if len(extracted_data['trendingProducts']) > 8:
                        print(f"   ... and {len(extracted_data['trendingProducts']) - 8} more")
                    break
        
        # Print exclusive deals
        if 'exclusiveDealsProducts' in extracted_data and extracted_data['exclusiveDealsProducts']:
            print("\n=== EXCLUSIVE DEALS ===")
            for i, deal in enumerate(extracted_data['exclusiveDealsProducts'], 1):
                print(f"{i}. {deal.get('name', 'N/A')} | Price: ₹{deal.get('cur_price', 'N/A')} (was ₹{deal.get('last_price', 'N/A')}, {deal.get('price_drop_per', 0)}% drop)")
                print(f"   Site: {deal.get('site_name', 'N/A')} | Score: {deal.get('score', 'N/A')}")
                if i >= 5:
                    if len(extracted_data['exclusiveDealsProducts']) > 5:
                        print(f"   ... and {len(extracted_data['exclusiveDealsProducts']) - 5} more")
                    break
        else:
            print("\n=== EXCLUSIVE DEALS ===\nNo deals extracted (fallback may miss them; check output.json for full data).")
        
        # Print features
        if 'features' in extracted_data and extracted_data['features']:
            print("\n=== FEATURES STATS ===")
            for key, value in extracted_data['features'].items():
                print(f"- {key}: {value}")
        
        # FIXED CSV: Include ALL fields from fallback (no more fieldnames error)
        if 'trendingProducts' in extracted_data and extracted_data['trendingProducts']:
            fields = ['name', 'cur_price', 'last_price', 'price_drop_per', 'site_name', 'rating', 'ratingCount', 'link', 'image', 'date', 'internalPid', 'site_pos', 'site_logo']
            with open('products.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(extracted_data['trendingProducts'])
            print("\nSUCCESS: Trending products exported to products.csv (open in Excel)")
        
        print("\n=== DONE! Check output.json, homepage.html, and products.csv ===")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
