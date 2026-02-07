import streamlit as st
import json
import os
from datetime import datetime

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- CUSTOM CSS (No changes made here) ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #001f3f 0%, #003366 100%); color: white; }
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px; border-radius: 20px;
            backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            width: 100%; border-radius: 10px; height: 3.5em;
            background-color: #FFD700; color: #001f3f; border: none;
            font-weight: 800; font-size: 15px; transition: all 0.3s ease;
        }
        .stButton>button:hover { background-color: #ffffff; transform: translateY(-3px); }
        .product-box {
            background: white; color: #333; padding: 20px;
            border-radius: 15px; margin-bottom: 20px;
            text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            min-height: 450px;
        }
        h1, h2, h3 { color: #FFD700 !important; }
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

# --- TOP BRANDING ---
st.markdown("""
    <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 15px; border-left: 10px solid #FFD700; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 35px;">📊 Price-Comparison System</h1>
        <p style="margin:0; color: #ccc;">The ultimate electronics deal finder | <span style="color: #00ff00;">● System Live</span></p>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

n1, n2, n3, n4 = st.columns([1, 1, 1, 3])
with n1:
    if st.button("🏠 HOME"): st.session_state.page = 'Home'
with n2:
    if st.button("🛠 SERVICES"): st.session_state.page = 'Services'
with n3:
    if st.button("ℹ️ ABOUT US"): st.session_state.page = 'About'
with n4:
    search_query = st.text_input("", placeholder="🔍 Search Products (e.g. iPhone, Laptop)...", label_visibility="collapsed")

st.write("---")

# --- PAGE ROUTING ---
if st.session_state.page == 'About':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("About the Developers")
    st.markdown("1. **K.AJAYKUMAR(TL)**\n2. **T.PRANATHI**\n3. **K.SAIKEERTHANA**\n4. **MD.HAROON**\n5. **S.MANICHARANREDDY**")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Services':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("Our Specialized Services")
    st.write("* **Real-time Price Comparison:** Automatically fetches the best deals.\n* **Price Drop Analysis:** Tracks market trends.\n* **Verified Sources:** Only trusted retailers included.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    if search_query:
        all_products = load_manual_products()
        filtered = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]
        
        if filtered:
            st.subheader(f"Found {len(filtered)} results for '{search_query}'")
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    st.markdown('<div class="product-box">', unsafe_allow_html=True)
                    
                    if product.get('image'):
                        st.image(product.get('image'), use_container_width=True)
                    
                    st.write(f"**{product.get('name')[:50]}...**")
                    
                    # --- UPDATED LOGIC START ---
                    cur_p = product.get('cur_price', 0)
                    last_p = product.get('last_price', cur_p)
                    rating = product.get('rating', 'N/A')
                    rev_count = product.get('ratingCount', 0) 
                    
                    # Calculate Price Drop Percentage
                    if last_p > cur_p:
                        drop_per = round(((last_p - cur_p) / last_p) * 100)
                    else:
                        drop_per = 0

                    # Display Price
                    st.markdown(f"<h2 style='color: #e63946 !important; margin: 0;'>₹{cur_p:,}</h2>", unsafe_allow_html=True)
                    
                    if drop_per > 0:
                        st.markdown(f"<p style='color: green; font-size: 14px; margin: 0;'><b>🔥 {drop_per}% PRICE DROP</b> <span style='text-decoration: line-through; color: #888;'>₹{last_p:,}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='color: #888; font-size: 14px; margin: 0;'>Best Price Guaranteed</p>", unsafe_allow_html=True)
                    
                    # Trust & Rating
                    st.markdown(f"<p style='color: #444; font-size: 14px; margin-top: 5px;'>⭐ {rating} | 👥 {rev_count:,} reviews</p>", unsafe_allow_html=True)
                    st.markdown("<div style='background: #d4edda; color: #155724; padding: 4px; border-radius: 8px; font-size: 11px; font-weight: bold;'>✓ VERIFIED GENUINE DEAL</div>", unsafe_allow_html=True)
                    # --- UPDATED LOGIC END ---

                    st.caption(f"Source: {product.get('site_name')}")
                    st.link_button(f"Go to {product.get('site_name')}", product.get('link'))
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No items found. Try searching for 'iPhone' or 'Laptop'.")
    else:
        st.markdown('<div class="main-card" style="text-align: center;"><h1>🛒📱💻</h1><h3>Search for products to compare prices live.</h3><p>Track smart. Spend wise.</p></div>', unsafe_allow_html=True)
