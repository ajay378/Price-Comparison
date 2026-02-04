import streamlit as st
import json
import os
import jinja2

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# Hide Sidebar and Header completely
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { margin-top: -80px; } /* Adjusting space because header is hidden */
    </style>
""", unsafe_allow_html=True)

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

# --- CSS & NAV BAR (Injecting directly for better control) ---
NAV_HTML = """
<div style="
    background-color: #002366;
    padding: 15px 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    font-family: 'Segoe UI', sans-serif;
    border-radius: 0 0 10px 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
">
    <div style="display: flex; align-items: center;">
        <div style="background: #FFD700; color: #002366; padding: 5px 12px; border-radius: 6px; font-weight: 900; margin-right: 15px;">PCS</div>
        <span style="font-size: 20px; font-weight: 600;">Price-Comparison System</span>
    </div>
    <div style="font-size: 16px;">
        Developed by <b>[Your Name]</b>
    </div>
</div>
"""

st.components.v1.html(NAV_HTML, height=80)

# --- NAVIGATION LOGIC USING STREAMLIT BUTTONS ---
# Same page navigation ke liye columns use kar rahe hain buttons ke liye
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = 'Home'
with col2:
    if st.button("🛠 Services"):
        st.session_state.page = 'Services'
with col3:
    if st.button("ℹ️ About Us"):
        st.session_state.page = 'About'

with col4:
    query = st.text_input("", placeholder="Search for electronics (e.g., iPhone, Laptop)...", label_visibility="collapsed")

# --- PAGE CONTENT ---
st.write("---") # Divider

if st.session_state.page == 'About':
    st.title("About Us")
    st.info("""
    ### Welcome!
    I am **[Your Name]**. This **Price-Comparison System** is built to help you find the best 
    electronics deals across the web in one single place.
    """)

elif st.session_state.page == 'Services':
    st.title("Our Services")
    st.success("✅ **Core Focus:** We compare electronics items only.")
    st.write("""
    - Real-time price updates for gadgets.
    - Comparison between major retailers like Amazon and Flipkart.
    - Simple and ad-free interface for quick decision making.
    """)

else: # Home Page & Search Logic
    if query:
        st.subheader(f"Search Results for: '{query}'")
        all_products = load_manual_products()
        filtered = [p for p in all_products if query.lower() in p.get('name', '').lower()]

        if filtered:
            # Displaying products in a clean grid
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    st.image(product.get('image', 'https://via.placeholder.com/150'), use_container_width=True)
                    st.write(f"**{product.get('name')}**")
                    st.error(f"Price: ₹{product.get('cur_price')}")
                    st.caption(f"Source: {product.get('site_name')}")
                    st.link_button("View Deal", product.get('link'))
        else:
            st.warning("No electronic items found for this search.")
    else:
        st.title("Welcome to Price-Comparison System")
        st.write("Use the search bar above to start comparing prices for your favorite tech gadgets.")
        st.image("https://via.placeholder.com/800x300/f9f9f9/002366?text=Best+Electronics+Deals+at+Your+Fingerprints", use_container_width=True)
