import json
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Site Logos Mapping (for product cards)
SITE_LOGOS = {
    'Flipkart': {'emoji': '🛒', 'logo_url': 'https://compare.buyhatke.com/images/site_icons_m/flipkart1.png'},
    'Amazon': {'emoji': '📦', 'logo_url': 'https://compare.buyhatke.com/images/site_icons_m/amazon.png'},
}

def load_manual_products():
    """Load products from products.json (only manual – no scraping)"""
    try:
        # Use absolute path based on the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        products_path = os.path.join(script_dir, 'products.json')
        
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                manual_products = json.load(f)
            print(f"DEBUG: Loaded {len(manual_products)} manual products from JSON")
            return manual_products
        else:
            print(f"DEBUG: No products.json found at {products_path} – no products available")
            return []
    except Exception as e:
        print(f"DEBUG: Error loading manual products: {e}")
        return []

@app.route('/')
def home():
    try:
        print("DEBUG: Starting home route...")
        return render_template_string(HOME_TEMPLATE, search_query="")
    except Exception as e:
        print(f"DEBUG: Home route error: {e}")
        return render_template_string(ERROR_TEMPLATE, error=f"App error: {str(e)}.")

@app.route('/search')
def search():
    try:
        query = request.args.get('q', '').lower().strip()
        print(f"DEBUG: Search query: '{query}'")

        if not query:
            return render_template_string(HOME_TEMPLATE, search_query="")

        all_products = load_manual_products()
        filtered_products = [p for p in all_products if query in p.get('name', '').lower()]

        for product in filtered_products:
            site = product.get('site_name', 'Flipkart')
            if 'logo_url' not in product:
                product['logo_url'] = SITE_LOGOS.get(site, {'logo_url': ''})['logo_url']
            if 'logo_emoji' not in product:
                product['logo_emoji'] = SITE_LOGOS.get(site, {'emoji': '🛒'})['emoji']

        print(f"DEBUG: Search returned {len(filtered_products)} products for '{query}'")
        return render_template_string(SEARCH_TEMPLATE, products=filtered_products, search_query=query)

    except Exception as e:
        print(f"DEBUG: Search route error: {e}")
        return render_template_string(ERROR_TEMPLATE, error=f"Search error: {str(e)}.")


# ------------------ HOME TEMPLATE ------------------
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Price Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 50px; background: #f4f4f4; }
        .header { 
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            margin-bottom: 20px;
        }
        .logo { 
            width: 50px !important;
            height: 41px !important;
            margin-right: 15px !important;
            border-radius: 5px;
            display: block !important;
            object-fit: contain;
            border: 2px solid #007BFF !important;
            background: #fff !important;
        }
        .title-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        h1 { color: #333; margin: 0; font-size: 28px; }
        .slogan { 
            font-size: 14px; 
            color: #666; 
            font-style: italic; 
            margin-top: 4px;
        }
        .search-bar { margin-top: 40px; margin-bottom: 30px; }
        .search-input { padding: 12px; width: 300px; border: 1px solid #ddd; border-radius: 25px; font-size: 16px; }
        .search-btn { padding: 12px 20px; background: #3498db; color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; margin-left: 10px; }
        .search-btn:hover { background: #2980b9; }
        .placeholder { color: #666; font-size: 18px; margin-top: 20px; }
        footer { margin-top: 50px; color: #999; }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="Logo" class="logo" 
             onerror="this.src='https://via.placeholder.com/50x41/FF6B6B/FFFFFF?text=PT'; this.style.border='2px solid red';">
        <div class="title-container">
            <h1>Price Tracker</h1>
            <p class="slogan">Track smart. Spend wise.</p>
        </div>
    </div>
    <div class="search-bar">
        <form action="/search" method="GET">
            <input type="text" name="q" placeholder="Search products (e.g., iPhone, Samsung)..." class="search-input" value="{{ search_query }}">
            <button type="submit" class="search-btn">Search</button>
        </form>
    </div>
    <div class="placeholder">
        <p>Enter a product name above to see prices, deals, and sites like Flipkart & Amazon.</p>
    </div>
    <footer>Manual catalog of 50+ products | Powered by Python & Flask</footer>
</body>
</html>
"""


# ------------------ SEARCH TEMPLATE ------------------
SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Price Tracker - Search Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f4; }
        .header { 
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            margin-bottom: 20px;
        }
        .logo { 
            width: 50px !important;
            height: 41px !important;
            margin-right: 15px !important;
            border-radius: 5px;
            display: block !important;
            object-fit: contain;
            border: 2px solid #007BFF !important;
            background: #fff !important;
        }
        .title-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        h1 { color: #333; margin: 0; font-size: 28px; }
        .slogan { 
            font-size: 14px; 
            color: #666; 
            font-style: italic; 
            margin-top: 4px;
        }
        .search-bar { text-align: center; margin-bottom: 30px; }
        .search-input { padding: 12px; width: 300px; border: 1px solid #ddd; border-radius: 25px; font-size: 16px; }
        .search-btn { padding: 12px 20px; background: #3498db; color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; margin-left: 10px; }
        .search-btn:hover { background: #2980b9; }
        .search-results { text-align: center; color: #666; margin-bottom: 20px; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .product-card { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .product-name { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #333; }
        .price { font-size: 24px; color: #e74c3c; font-weight: bold; margin-bottom: 10px; }
        .site { display: flex; align-items: center; margin: 10px 0; }
        .site-logo { width: 40px; height: 40px; margin-right: 10px; border-radius: 5px; }
        .rating { color: #f39c12; margin: 10px 0; }
        .link { background: #3498db; color: white; padding: 8px 12px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }
        .link:hover { background: #2980b9; }
        .product-image { width: 100%; max-height: 200px; object-fit: cover; border-radius: 5px; margin-top: 10px; }
        .no-results { text-align: center; color: #666; margin: 50px; }
        footer { text-align: center; margin-top: 40px; color: #999; }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="Logo" class="logo" 
             onerror="this.src='https://via.placeholder.com/50x41/FF6B6B/FFFFFF?text=PT'; this.style.border='2px solid red';">
        <div class="title-container">
            <h1>Price Tracker</h1>
            <p class="slogan">Track smart. Spend wise.</p>
        </div>
    </div>
    <div class="search-bar">
        <form action="/search" method="GET">
            <input type="text" name="q" placeholder="Search products (e.g., iPhone, Samsung)..." class="search-input" value="{{ search_query }}">
            <button type="submit" class="search-btn">Search</button>
        </form>
    </div>
    <div class="search-results">
        <h2>Results for "{{ search_query }}": {{ products|length }} products found</h2>
    </div>
    {% if products %}
    <div class="product-grid">
        {% for product in products %}
        <div class="product-card">
            <div class="product-name">{{ product.name }}</div>
            <div class="price">₹{{ product.cur_price }} ({{ product.price_drop_per }}% off from ₹{{ product.last_price }})</div>
            <div class="site">
                <img src="{{ product.logo_url }}" alt="{{ product.site_name }}" class="site-logo" onerror="this.style.display='none';">
                <span>{{ product.logo_emoji }} {{ product.site_name }}</span>
            </div>
            <div class="rating">⭐ {{ product.rating }} ({{ product.ratingCount }} reviews)</div>
            <img src="{{ product.image }}" alt="{{ product.name }}" class="product-image" 
                 onerror="this.src='https://via.placeholder.com/300x200?text={{ product.name[:10] }}';">
            <a href="{{ product.link }}" class="link" target="_blank">View on Site</a>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="no-results">
        <p>No products found for "{{ search_query }}". Try "iPhone", "Samsung", or "Sony".</p>
    </div>
    {% endif %}
    <footer>Manual catalog of 50+ products | Powered by Python & Flask</footer>
</body>
</html>
"""


# ------------------ ERROR TEMPLATE ------------------
ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Price Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 50px; background: #f4f4f4; }
        .header { 
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            margin-bottom: 20px;
        }
        .logo { 
            width: 50px !important;
            height: 41px !important;
            margin-right: 15px !important;
            border-radius: 5px;
            display: block !important;
            object-fit: contain;
            border: 2px solid #007BFF !important;
            background: #fff !important;
        }
        .title-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        h1 { color: #333; margin: 0; font-size: 28px; }
        .slogan { 
            font-size: 14px; 
            color: #666; 
            font-style: italic; 
            margin-top: 4px;
        }
        .error { color: #e74c3c; font-size: 18px; margin: 20px; }
        .search-bar { margin-bottom: 30px; }
        .search-input { padding: 12px; width: 300px; border: 1px solid #ddd; border-radius: 25px; font-size: 16px; }
        .search-btn { padding: 12px 20px; background: #3498db; color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; margin-left: 10px; }
        .search-btn:hover { background: #2980b9; }
        footer { margin-top: 50px; color: #999; }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="Logo" class="logo" 
             onerror="this.src='https://via.placeholder.com/50x41/FF6B6B/FFFFFF?text=PT'; this.style.border='2px solid red';">
        <div class="title-container">
            <h1>Price Tracker</h1>
            <p class="slogan">Track smart. Spend wise.</p>
        </div>
    </div>
    <div class="error">
        <h2>Oops! Something went wrong.</h2>
        <p>{{ error }}</p>
        <p>Try searching again or refresh the page.</p>
    </div>
    <div class="search-bar">
        <form action="/search" method="GET">
            <input type="text" name="q" placeholder="Search products (e.g., iPhone, Samsung)..." class="search-input">
            <button type="submit" class="search-btn">Search</button>
        </form>
    </div>
    <footer>Manual catalog | Powered by Python & Flask</footer>
</body>
</html>
"""


# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    application = app
