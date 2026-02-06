import streamlit as st
import json
import os

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- CLEAN CSS (Removing Blank Boxes & Extra Gaps) ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #001f3f 0%, #003366 100%); color: white; }
        
        /* Product Card Fix */
        .product-box {
            background: white; color: #333; padding: 15px;
            border-radius: 12px; margin: 0px;
            text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            height: 100%;
        }
        
        .product-box p, .product-box h4, .product-box b { color: #333 !important; margin: 2px 0; }
        
        /* Navigation Buttons */
        .stButton>button {
            width: 100%; border-radius: 8px; height: 3em;
            background-color: #FFD700; color: #001f3f; border: none; font-weight: 800;
        }
        
        /* Removing extra white space at the top */
        .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
        
        /* Hiding empty streamlit elements */
        div[data-testid="stVerticalBlock"] > div:empty { display: none; }
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
    except: return []

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'Home'

# Header
st.markdown('<h1 style="color: #FFD700; margin-bottom: 0;">📊 Price-Comparison System</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #ccc; margin-top: 0;">Verified Amazon & Flipkart Deals</p>', unsafe_allow_html=True)

# Menu
n1, n2, n3, n4 = st.columns([1, 1, 1, 3])
with n1:
    if st.button("HOME"):
        st.session_state.page = 'Home'
        st.query_params.clear()
        st.rerun()
with n2:
    if st.button("SERVICES"):
        st.session_state.page = 'Services'
        st.query_params.clear()
        st.rerun()
with n3:
    if st.button("ABOUT US"):
        st.session_state.page = 'About'
        st.query_params.clear()
        st.rerun()
with n4:
    search_query = st.text_input("", placeholder="🔍 Search Electronics...", label_visibility="collapsed", key="clean_search")

st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

# --- MAIN LOGIC ---
if search_query:
    all_products = load_manual_products()
    filtered = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]
    
    if filtered:
        st.markdown(f"### Results for '{search_query}'")
        cols = st.columns(3)
        for idx, product in enumerate(filtered):
            with cols[idx % 3]:
                # Data Prep
                cur_p = product.get('cur_price', 0)
                last_p = product.get('last_price', cur_p)
                drop = product.get('price_drop_per', 0)
                
                # Clean Card (No extra divs)
                st.markdown(f'''
                    <div class="product-box">
                        <img src="{product.get('image')}" style="width:100%; border-radius:8px;">
                        <h4 style="font-size:14px;">{product.get('name')[:45]}...</h4>
                        <h2 style="color:#d62828; margin:5px 0;">₹{cur_p:,}</h2>
                        <p style="color:green; font-size:12px;"><b>{drop}% OFF</b> <s>₹{last_p:,}</s></p>
                        <p style="font-size:12px;">⭐ {product.get('rating')} | {product.get('site_name')}</p>
                    </div>
                ''', unsafe_allow_html=True)
                st.link_button(f"GO TO {product.get('site_name').upper()}", product.get('link'))
    else:
        st.error("No items found.")

else:
    # Pages
    if st.session_state.page == 'About':
        st.title("About the Developers")
        st.write("1. K.AJAYKUMAR (TL)\n2. T.PRANATHI\n3. K.SAIKEERTHANA\n4. MD.HAROON\n5. S.MANICHARANREDDY")
    elif st.session_state.page == 'Services':
        st.title("Our Specialized Services")
        st.warning("Policy: Electronics only.")
        st.write("* Price Comparison\n* Retailer Redirects\n* Ad-free Experience")
    else:
        st.title("Welcome to Price-Comparison System")
        st.info("Use the search bar to find deals.")

st.markdown("<br><p style='text-align: center; color: #777;'>© 2026 Price-Comparison System</p>", unsafe_allow_html=True)
