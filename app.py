import streamlit as st
import json
import os

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- IMPROVED CSS ---
st.markdown("""
    <style>
        .stApp { 
            background: linear-gradient(135deg, #001f3f 0%, #003366 100%); 
            color: #ffffff; 
        }
        
        /* Product Card Styling */
        .product-box {
            background: #ffffff;
            color: #1a1a1a;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
        
        .product-box p, .product-box h4, .product-box span {
            color: #1a1a1a !important;
        }

        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #FFD700;
            color: #001f3f;
            font-weight: bold;
        }

        h1, h2, h3 { color: #FFD700 !important; }
        
        /* Removes extra white space/boxes above products */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
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
    except: return []

# --- TOP BRANDING ---
st.markdown("""
    <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 15px; border-left: 10px solid #FFD700; margin-bottom: 20px;">
        <h1 style="margin:0; font-size: 32px;">📊 Price-Comparison System</h1>
        <p style="margin:0; color: #eeeeee;">Premium Electronics Price Tracker</p>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'Home'

# --- NAVIGATION & SEARCH ---
n1, n2, n3, n4 = st.columns([1, 1, 1, 3])
with n1: 
    if st.button("HOME"): st.session_state.page = 'Home'
with n2: 
    if st.button("SERVICES"): st.session_state.page = 'Services'
with n3: 
    if st.button("ABOUT US"): st.session_state.page = 'About'
with n4: 
    search_query = st.text_input("", placeholder="🔍 Search Products...", label_visibility="collapsed")

st.write("---")

# --- CORE LOGIC (Search Everywhere Fix) ---

# Agar user ne search bar mein kuch likha hai, toh wahi dikhao (chahe wo kisi bhi page pe ho)
if search_query:
    all_products = load_manual_products()
    filtered = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]
    
    if filtered:
        st.subheader(f"Results for '{search_query}'")
        cols = st.columns(3)
        for idx, product in enumerate(filtered):
            with cols[idx % 3]:
                # Extracting Data
                cur_p = product.get('cur_price', 0)
                last_p = product.get('last_price', cur_p)
                rating = product.get('rating', 'N/A')
                rev_count = product.get('ratingCount', 0)
                drop = product.get('price_drop_per', 0)
                
                st.markdown('<div class="product-box">', unsafe_allow_html=True)
                
                if product.get('image'):
                    st.image(product.get('image'), use_container_width=True)
                
                st.markdown(f"<h4>{product.get('name')[:50]}...</h4>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='color: #d62828 !important; margin: 0;'>₹{cur_p:,}</h2>", unsafe_allow_html=True)
                
                if drop > 0:
                    st.markdown(f"<p style='color: #2b9348; font-size: 14px;'><b>{drop}% OFF</b> <s>₹{last_p:,}</s></p>", unsafe_allow_html=True)
                
                st.markdown(f"<p style='font-size: 14px;'>⭐ {rating} | 👥 {rev_count:,} Reviews</p>", unsafe_allow_html=True)
                st.link_button(f"VIEW ON {product.get('site_name').upper()}", product.get('link'))
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("No items found.")

# Agar search bar khali hai, toh regular pages dikhao
else:
    if st.session_state.page == 'About':
        st.title("About the Developers")
        st.markdown("""
        1. **K.AJAYKUMAR (TL)**
        2. **T.PRANATHI**
        3. **K.SAIKEERTHANA**
        4. **MD.HAROON**
        5. **S.MANICHARANREDDY**
        """)
    elif st.session_state.page == 'Services':
        st.title("Our Specialized Services")
        st.write("* Real-time Price Comparison\n* Retailer Redirection\n* Deal Analytics")
    else:
        # HOME PAGE
        st.markdown('<div style="text-align: center; padding: 30px;">', unsafe_allow_html=True)
        st.title("Welcome to Price-Comparison System")
        st.write("Find the best deals on premium electronics.")
        st.markdown("<h1 style='font-size: 80px;'>🛒📱💻</h1>", unsafe_allow_html=True)
        st.info("Search above to see products.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; margin-top: 50px;'>© 2026 Price-Comparison System</p>", unsafe_allow_html=True)
