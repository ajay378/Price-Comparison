import streamlit as st
import json
import os
import jinja2

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

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

# --- UPDATED HTML TEMPLATE (ENGLISH) ---
LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f9f9f9; color: #333; }
        
        /* Navigation Bar */
        .navbar {
            background-color: #002366; /* Royal Blue */
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 50px;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .logo-section { display: flex; align-items: center; }
        .logo-box { 
            background: #FFD700; color: #002366; padding: 5px 10px; 
            border-radius: 8px; font-weight: 900; font-size: 20px; margin-right: 12px;
        }
        .logo-text { font-size: 22px; font-weight: 600; letter-spacing: 0.5px; }
        
        .nav-links { list-style: none; display: flex; margin: 0; padding: 0; }
        .nav-links li { margin: 0 20px; }
        .nav-links a { color: #ffffff; text-decoration: none; font-size: 15px; font-weight: 500; transition: 0.3s; }
        .nav-links a:hover { color: #FFD700; }

        /* Search Bar */
        .search-box { display: flex; }
        .search-box input { 
            padding: 10px 15px; border: none; border-radius: 20px 0 0 20px; 
            outline: none; width: 280px; font-size: 14px;
        }
        .search-box button { 
            padding: 10px 20px; background: #FFD700; border: none; 
            color: #002366; cursor: pointer; border-radius: 0 20px 20px 0; font-weight: bold;
        }

        /* Main Content */
        .container { padding: 60px 10%; text-align: center; min-height: 70vh; }
        h1 { color: #002366; font-size: 36px; margin-bottom: 20px; }
        .info-card { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }

        /* Product Display */
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-top: 40px; }
        .product-card { 
            background: white; border-radius: 12px; padding: 20px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: left;
            transition: 0.3s;
        }
        .product-card:hover { transform: translateY(-8px); }
        .product-image { width: 100%; height: 180px; object-fit: contain; margin-bottom: 15px; }
        .price { font-size: 22px; color: #e63946; font-weight: bold; }
        .site-badge { background: #f1f1f1; padding: 3px 10px; border-radius: 20px; font-size: 12px; color: #555; }
        
        footer { background: #002366; color: white; padding: 20px; text-align: center; margin-top: 50px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo-section">
            <div class="logo-box">PCS</div>
            <span class="logo-text">Price-Comparison System</span>
        </div>
        
        <ul class="nav-links">
            <li><a href="?page=home">Home</a></li>
            <li><a href="?page=services">Services</a></li>
            <li><a href="?page=about">About Us</a></li>
        </ul>

        <form action="/" method="get" class="search-box">
            <input type="text" name="q" placeholder="Search for electronics..." value="{{ query }}">
            <button type="submit">Search</button>
        </form>
    </nav>

    <div class="container">
        {% if page == 'about' %}
            <div class="info-card">
                <h1>About Us</h1>
                <p style="font-size: 18px; line-height: 1.6;">
                    Hello! I am <strong>[Your Name Here]</strong>. <br>
                    Welcome to the <strong>Price-Comparison System</strong>. This platform is designed 
                    to help users find the best deals across various e-commerce websites effortlessly.
                </p>
            </div>
        {% elif page == 'services' %}
            <div class="info-card">
                <h1>Our Services</h1>
                <p style="font-size: 20px; color: #e63946; font-weight: bold;">We compare electronics items only.</p>
                <p>We provide real-time price comparisons for smartphones, laptops, headphones, and other high-tech gadgets to ensure you never overpay.</p>
            </div>
        {% else %}
            {% if query %}
                <h1>Search Results for "{{ query }}"</h1>
                <div class="product-grid">
                    {% for product in products %}
                    <div class="product-card">
                        <img src="{{ product.image }}" class="product-image">
                        <div style="font-weight: 600; margin-bottom: 8px;">{{ product.name }}</div>
                        <div class="price">₹{{ product.cur_price }}</div>
                        <span class="site-badge">{{ product.site_name }}</span>
                        <br><br>
                        <a href="{{ product.link }}" target="_blank" style="color: #002366; font-weight: bold; text-decoration: none;">Check Deal →</a>
                    </div>
                    {% endfor %}
                </div>
                {% if not products %} <p>No electronic items found for this search.</p> {% endif %}
            {% else %}
                <div style="margin-top: 50px;">
                    <h1>Find the Best Tech Deals</h1>
                    <p style="font-size: 18px; color: #666;">Compare prices for top electronics and save money instantly.</p>
                    <img src="https://via.placeholder.com/600x300/f9f9f9/002366?text=Electronic+Price+Comparison" style="max-width: 100%; border-radius: 10px; margin-top: 20px;">
                </div>
            {% endif %}
        {% endif %}
    </div>

    <footer>
        &copy; 2026 Price-Comparison System | Developed by [Your Name Here]
    </footer>
</body>
</html>
"""

# --- LOGIC TO HANDLE URL PARAMS ---
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

# Display HTML
st.components.v1.html(html_content, height=1200, scrolling=True)

# Hide Sidebar and Streamlit branding
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
