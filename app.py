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
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        products_path = os.path.join(script_dir, 'products.json')
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        return []

# --- NEW TEMPLATE WITH INTEGRATED NAV BAR ---
# Isme Sidebar nahi hai, sab kuch top nav bar mein hai.
LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f4f4f4; }
        
        /* Navigation Bar Styling */
        .navbar {
            background-color: #333;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 50px;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .logo-section { display: flex; align-items: center; }
        .logo-img { width: 40px; height: 40px; margin-right: 10px; border-radius: 5px; }
        .nav-links { list-style: none; display: flex; margin: 0; padding: 0; }
        .nav-links li { margin: 0 20px; }
        .nav-links a { color: white; text-decoration: none; font-weight: 500; }
        .nav-links a:hover { color: #ff9800; }

        /* Search Bar in Nav */
        .search-box { display: flex; }
        .search-box input { padding: 8px; border: none; border-radius: 4px 0 0 4px; outline: none; width: 250px; }
        .search-box button { 
            padding: 8px 15px; 
            background: #ff9800; 
            border: none; 
            color: white; 
            cursor: pointer; 
            border-radius: 0 4px 4px 0; 
        }

        /* Product Grid */
        .container { padding: 40px; text-align: center; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
        .product-card { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: left; }
        .product-image { width: 100%; height: 180px; object-fit: contain; }
        .price { font-size: 22px; color: #e74c3c; font-weight: bold; }
        footer { margin-top: 50px; color: #888; padding: 20px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo-section">
            <img src="https://via.placeholder.com/40/FF9800/FFFFFF?text=PT" class="logo-img">
            <span style="font-size: 20px; font-weight: bold;">PriceTracker</span>
        </div>
        
        <ul class="nav-links">
            <li><a href="?page=home">Home</a></li>
            <li><a href="?page=services">Services</a></li>
            <li><a href="?page=about">About Us</a></li>
        </ul>

        <form action="/" method="get" class="search-box">
            <input type="text" name="q" placeholder="Product ka naam dalein..." value="{{ query }}">
            <button type="submit">Search</button>
        </form>
    </nav>

    <div class="container">
        {% if page == 'about' %}
            <h1>About Us</h1>
            <p>Hum aapko sabse saste prices dhundhne mein madad karte hain.</p>
        {% elif page == 'services' %}
            <h1>Our Services</h1>
            <p>Price Tracking, Alert Notifications, aur Detailed Analytics.</p>
        {% else %}
            {% if query %}
                <h2>Results for "{{ query }}"</h2>
                <div class="product-grid">
                    {% for product in products %}
                    <div class="product-card">
                        <img src="{{ product.image }}" class="product-image">
                        <div style="font-weight: bold; margin-top:10px;">{{ product.name }}</div>
                        <div class="price">₹{{ product.cur_price }}</div>
                        <small>{{ product.site_name }}</small><br>
                        <a href="{{ product.link }}" target="_blank" style="color: #3498db;">View Deal</a>
                    </div>
                    {% endfor %}
                </div>
                {% if not products %} <p>Koi product nahi mila!</p> {% endif %}
            {% else %}
                <h1>Welcome to Price Tracker</h1>
                <p>Upar search bar mein product ka naam dalkar search karein.</p>
            {% endif %}
        {% endif %}
    </div>

    <footer>© 2026 Price Tracker India</footer>
</body>
</html>
"""

# --- LOGIC TO HANDLE URL PARAMS ---
# Streamlit mein navigation aur search url query se handle karenge
params = st.query_params
current_page = params.get("page", "home")
search_query = params.get("q", "")

filtered_products = []
if search_query:
    all_products = load_manual_products()
    filtered_products = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]

# Render Jinja2
t = jinja2.Template(LAYOUT_TEMPLATE)
html_content = t.render(
    page=current_page, 
    query=search_query, 
    products=filtered_products
)

# Display
st.components.v1.html(html_content, height=1500, scrolling=True)

# Sidebar ko hide karne ke liye CSS (Just in case Streamlit default dikhaye)
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)
