import streamlit as st
import json
import os
from datetime import datetime

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- FIXED CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #001f3f 0%, #003366 100%); color: white; }
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main Card Style */
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px; border-radius: 20px;
            backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }

        /* Product Card Style - Fixed for alignment */
        .product-box {
            background: white; 
            color: #333; 
            padding: 15px;
            border-radius: 15px; 
            margin-bottom: 20px;
            text-align: center; 
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        h1, h2, h3 { color: #FFD700 !important; }
        
        /* Button Styling inside card */
        .stButton>button {
            border-radius: 10px;
            background-color: #FFD700; 
            color: #001f3f;
            font-weight: 800;
        }
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
        <p style="margin:0; color: #ccc;">Verified Deals | <span style="color: #00ff00;">● System Live</span></p>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Navigation
n1, n2, n3, n4 = st.columns([1, 1, 1, 3])
with n1:
    if st.button("🏠 HOME"): st.session_state.page = 'Home'
with n2:
    if st.button("🛠 SERVICES"): st.session_state.page = 'Services'
with n3:
    if st.button("ℹ️ ABOUT US"): st.session_state.page = 'About'
with n4:
    search_query = st.text_input("", placeholder="🔍 Search Products...", label_visibility="collapsed")

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
    st.write("* Real-time Price Comparison\n* Price Drop Alerts\n* Verified Seller Links")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    if search_query:
        all_products = load_manual_products()
        filtered = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]
        
        if filtered:
            st.subheader(f"Showing results for '{search_query}'")
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    # Start of White Box (Card)
                    st.markdown('<div class="product-box">', unsafe_allow_html=True)
                    
                    # 1. Product Image
                    if product.get('image'):
                        st.image(product.get('image'), use_container_width=True)
                    
                    # 2. Product Name
                    st.markdown(f"<h4 style='color: #333; height: 50px; overflow: hidden;'>{product.get('name')[:45]}...</h4>", unsafe_allow_html=True)
                    
                    # 3. Price & Drop Calculation
                    cur_p = product.get('cur_price', 0)
                    last_p = product.get('last_price', cur_p)
                    drop_per = round(((last_p - cur_p) / last_p) * 100) if last_p > cur_p else 0

                    st.markdown(f"<h2 style='color: #e63946; margin: 0;'>₹{cur_p:,}</h2>", unsafe_allow_html=True)
                    
                    if drop_per > 0:
                        st.markdown(f"<p style='color: green; font-size: 14px;'><b>🔥 {drop_per}% OFF</b></p>", unsafe_allow_html=True)
                    
                    # 4. Verification Badge
                    st.markdown("<div style='background: #d4edda; color: #155724; padding: 5px; border-radius: 5px; font-size: 10px; font-weight: bold; margin-bottom: 10px;'>✓ VERIFIED GENUINE</div>", unsafe_allow_html=True)
                    
                    # 5. Buy Button (Placed inside the card)
                    st.link_button(f"Go to {product.get('site_name')}", product.get('link'), use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True) # End of Box
        else:
            st.error("No items found.")
    else:
        st.markdown('<div class="main-card" style="text-align: center;"><h1>🛒</h1><h3>Search for electronics to compare prices.</h3></div>', unsafe_allow_html=True)
