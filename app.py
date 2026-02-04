import streamlit as st
import json
import os
import jinja2

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price Tracker", page_icon="🛒", layout="wide")

# Site Logos Mapping
SITE_LOGOS = {
    'Flipkart': {'emoji': '🛒', 'logo_url': 'https://compare.buyhatke.com/images/site_icons_m/flipkart1.png'},
    'Amazon': {'emoji': '📦', 'logo_url': 'https://compare.buyhatke.com/images/site_icons_m/amazon.png'},
}

def load_manual_products():
    """Load products from products.json"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        products_path = os.path.join(script_dir, 'products.json')
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        return []

# Jinja2 setup to render templates like Flask does
def render_template_string(template_str, **context):
    return jinja2.Template(template_str).render(**context)

# ------------------ TEMPLATES (As provided by you) ------------------
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 50px; background: #f4f4f4; }
        .header { display: flex; align-items: center; justify-content: flex-start; background: #f8f9fa; padding: 20px; border-bottom: 1px solid #dee2e6; margin-bottom: 20px; }
        .logo { width: 50px; height: 41px; margin-right: 15px; border-radius: 5px; border: 2px solid #007BFF; background: #fff; }
        .title-container { display: flex; flex-direction: column; align-items: flex-start; }
        h1 { color: #333; margin: 0; font-size: 28px; }
        .slogan { font-size: 14px; color: #666; font-style: italic; margin-top: 4px; }
        footer { margin-top: 50px; color: #999; }
    </style>
</head>
<body>
    <div class="header">
        <img src="https://via.placeholder.com/50x41/FF6B6B/FFFFFF?text=PT" alt="Logo" class="logo">
        <div class="title-container">
            <h1>Price Tracker</h1>
            <p class="slogan">Track smart. Spend wise.</p>
        </div>
    </div>
    <div style="margin-top: 40px;">
        <p style="color: #666; font-size: 18px;">Enter a product name in the sidebar to see prices!</p>
    </div>
    <footer>Manual catalog of 50+ products | Powered by Streamlit</footer>
</body>
</html>
"""

SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f4; }
        .header { display: flex; align-items: center; justify-content: flex-start; background: #f8f9fa; padding: 20px; border-bottom: 1px solid #dee2e6; margin-bottom: 20px; }
        .logo { width: 50px; height: 41px; margin-right: 15px; border-radius: 5px; border: 2px solid #007BFF; background: #fff; }
        .title-container { display: flex; flex-direction: column; align-items: flex-start; }
        h1 { color: #333; margin: 0; font-size: 28px; }
        .slogan { font-size: 14px; color: #666; font-style: italic; margin-top: 4px; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .product-card { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: left; }
        .product-name { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #333; }
        .price { font-size: 24px; color: #e74c3c; font-weight: bold; margin-bottom: 10px; }
        .site { display: flex; align-items: center; margin: 10px 0; }
        .site-logo { width: 30px; height: 30px; margin-right: 10px; }
        .link { background: #3498db; color: white; padding: 8px 12px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }
        .product-image { width: 100%; max-height: 200px; object-fit: contain; border-radius: 5px; }
        footer { text-align: center; margin-top: 40px; color: #999; }
    </style>
</head>
<body>
    <div class="header">
        <img src="https://via.placeholder.com/50x41/FF6B6B/FFFFFF?text=PT" alt="Logo" class="logo">
        <div class="title-container">
            <h1>Price Tracker</h1>
            <p class="slogan">Track smart. Spend wise.</p>
        </div>
    </div>
    <h2 style="text-align: center; color: #666;">Results for "{{ search_query }}": {{ products|length }} products found</h2>
    <div class="product-grid">
        {% for product in products %}
        <div class="product-card">
            <div class="product-name">{{ product.name }}</div>
            <div class="price">₹{{ product.cur_price }} ({{ product.price_drop_per }}% off)</div>
            <div class="site">
                <img src="{{ product.logo_url }}" class="site-logo">
                <span>{{ product.logo_emoji }} {{ product.site_name }}</span>
            </div>
            <img src="{{ product.image }}" class="product-image">
            <a href="{{ product.link }}" class="link" target="_blank">View on Site</a>
        </div>
        {% endfor %}
    </div>
    <footer>Powered by Python & Streamlit</footer>
</body>
</html>
"""

# --- MAIN STREAMLIT LOGIC ---
st.sidebar.title("Search Panel")
query = st.sidebar.text_input("Product Name", placeholder="e.g. iPhone")

if query:
    all_products = load_manual_products()
    filtered_products = [p for p in all_products if query.lower() in p.get('name', '').lower()]
    
    # Add logos to filtered products
    for product in filtered_products:
        site = product.get('site_name', 'Flipkart')
        if 'logo_url' not in product:
            product['logo_url'] = SITE_LOGOS.get(site, {'logo_url': ''})['logo_url']
        if 'logo_emoji' not in product:
            product['logo_emoji'] = SITE_LOGOS.get(site, {'emoji': '🛒'})['emoji']

    html_to_display = render_template_string(SEARCH_TEMPLATE, products=filtered_products, search_query=query)
else:
    html_to_display = render_template_string(HOME_TEMPLATE)

# Display the HTML in Streamlit
st.components.v1.html(html_to_display, height=1200, scrolling=True)
