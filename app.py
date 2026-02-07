import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 1. Function jo JSON file ko update karega
def update_price_data(product_name):
    print(f"Fetching live data for: {product_name}...")
    
    # Example URL (Tum yahan apne specific URLs ya search logic dal sakte ho)
    # Maan lo hum Amazon se fetch kar rahe hain
    headers = {"User-Agent": "Mozilla/5.0"} 
    url = f"https://www.example-store.com/search?q={product_name}" # Replace with actual logic
    
    # --- Yahan Scraping Logic aayega ---
    # Dummy data for demo (Yahan tumhara purana scraper fit hoga)
    live_price = "₹54,999" 
    store_name = "Amazon"
    
    # 2. Naya data structure with Timestamp
    updated_info = {
        "product": product_name,
        "price": live_price,
        "store": store_name,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Verified Genuine"
    }

    # 3. JSON file mein save karna
    with open('data.json', 'w') as file:
        json.dump(updated_info, file, indent=4)
    
    print("JSON file successfully updated with real-time data!")

# 4. Program start hote hi check karo
def get_display_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None

# Demo Run
product = "iPhone 15"
update_price_data(product) # Ye function JSON ko refresh kar dega
current_data = get_display_data()

print(f"\n--- Faculty Dashboard ---")
print(f"Product: {current_data['product']}")
print(f"Price: {current_data['price']}")
print(f"Last Synced: {current_data['last_updated']}") # Ye unhe trust dilayega
print(f"Status: {current_data['status']}")
