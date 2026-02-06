import streamlit as st
import json
import os

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- CUSTOM CSS (Strictly Original) ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #001f3f 0%, #003366 100%); color: white; }
        .product-box {
            background: white; color: #333; padding: 20px;
            border-radius: 15px; margin-bottom: 20px;
            text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .product-box p, .product-box h4, .product-box b, .product-box span { color: #333 !important; }
        .stButton>button {
            width: 100%; border-radius: 10px; height: 3.5em;
            background-color: #FFD700; color: #001f3f; border: none; font-weight: 800;
        }
        h1, h2, h3 { color: #FFD700 !important; }
        .block-container { padding-top: 1rem; }
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

# --- NAVIGATION LOGIC ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# --- TOP BRANDING ---
st.markdown("""
    <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 15px; border-left: 10px solid #FFD700; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 35px;">📊 Price-Comparison System</h1>
        <p style="margin:0; color: #ccc;">The ultimate electronics deal finder</p>
    </div>
""", unsafe_allow_html=True)

# Navigation Buttons
n1, n2, n3, n4 = st.columns([1, 1, 1, 3])

with n1:
    if st.button("🏠 HOME"):
        st.session_state.page = 'Home'
        # Force clear everything to fix the button freeze
        st.query_params.clear() 
        st.rerun() 
with n2:
    if st.button("🛠 SERVICES"):
        st.session_state.page = 'Services'
        st.query_params.clear()
        st.rerun()
with n3:
    if st.button("ℹ️ ABOUT US"):
        st.session_state.page = 'About'
        st.query_params.clear()
        st.rerun()
with n4:
    # Adding a unique key ensures the bar resets when we rerun
    search_query = st.text_input("", placeholder="🔍 Search Products...", label_visibility="collapsed", key="user_search")

st.write("---")

# --- MAIN DISPLAY LOGIC ---

# 1. First priority: Search results
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
                st.write(f"**{product.get('name')}**")
                
                cur_p = product.get('cur_price', 0)
                last_p = product.get('last_price', cur_p)
                drop = product.get('price_drop_per', 0)
                rating = product.get('rating', 'N/A')
                rev_count = product.get('ratingCount', 0)

                st.markdown(f"<h2 style='color: #e63946 !important; margin:0;'>₹{cur_p:,}</h2>", unsafe_allow_html=True)
                if drop > 0:
                    st.markdown(f"<p style='color: green; margin:0;'><b>{drop}% OFF</b> <s>₹{last_p:,}</s></p>", unsafe_allow_html=True)
                
                st.markdown(f"<p style='margin-top:5px;'>⭐ {rating} | 👥 {rev_count:,} reviews</p>", unsafe_allow_html=True)
                st.caption(f"Source: {product.get('site_name')}")
                st.link_button(f"Go to {product.get('site_name')}", product.get('link'))
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("No electronic items found.")

# 2. Second priority: Show Page Content only if NO search is happening
else:
    if st.session_state.page == 'About':
        st.title("About the Developers")
        st.markdown("""
        ### Project Developed By Team:
        1. **K.AJAYKUMAR(TL)**
        2. **T.PRANATHI**
        3. **K.SAIKEERTHANA**
        4. **MD.HAROON**
        5. **S.MANICHARANREDDY**
        
        ---
        **Vision:** Our mission is to simplify tech shopping by providing a unified platform to compare prices of premium electronics across the major retailers in India.
        """)

    elif st.session_state.page == 'Services':
        st.title("Our Specialized Services")
        st.warning("### 🚨 Policy: We compare electronics items only.")
        st.write("""
        We specialize in:
        * **Real-time Price Comparison** for all Premium Electronics.
        * **Direct Redirects** to verified retailers.
        * **Clean Ad-free Experience** for quick shopping.
        """)

    else:
        # HOME PAGE
        st.markdown('<div style="text-align: center; padding: 30px;">', unsafe_allow_html=True)
        st.title("Welcome to Price-Comparison System")
        st.write("### Track smart. Spend wise.")
        st.markdown("<h1 style='font-size: 100px;'>🛒📱💻</h1>", unsafe_allow_html=True)
        st.write("Start your search today and save thousands on your next tech purchase.")
        st.info("💡 **How to use:** Simply type the name of a gadget in the search bar above.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777;'>© 2026 Price-Comparison System | Electronics Only</p>", unsafe_allow_html=True)
