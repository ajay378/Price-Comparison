import streamlit as st
import json
import os
import jinja2

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# CSS for Highlighting Buttons and Hiding Sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Buttons Highlight */
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #002366;
            color: white;
            border: 2px solid #FFD700;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #FFD700;
            color: #002366;
            border: 2px solid #002366;
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

# --- TOP NAVIGATION BAR (HTML for Logo) ---
NAV_HTML = """
<div style="
    background-color: #002366;
    padding: 15px 50px;
    display: flex;
    align-items: center;
    color: white;
    font-family: 'Segoe UI', sans-serif;
    border-radius: 10px;
    margin-bottom: 20px;
">
    <div style="background: #FFD700; color: #002366; padding: 5px 12px; border-radius: 6px; font-weight: 900; margin-right: 15px;">PCS</div>
    <span style="font-size: 24px; font-weight: 600;">Price-Comparison System</span>
</div>
"""
st.components.v1.html(NAV_HTML, height=80)

# --- NAVIGATION LOGIC ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

col1, col2, col3, col4 = st.columns([1, 1, 1, 3])

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
    # Text input for search
    query = st.text_input("", placeholder="Search electronic products (iPhone, Laptop...)", label_visibility="collapsed")

st.write("---")

# --- PAGE CONTENT ---

if st.session_state.page == 'About':
    st.title("About Us")
    st.markdown("""
    ### Project Developed By:
    1. **Ajay Konda**
    2. **Pranati**
    3. **Sai Keerthana**
    4. **Haroon**
    5. **Mani Charan**
    
    ---
    **Price-Comparison System** is a platform built to provide the best electronics deals across various e-commerce sites.
    """)

elif st.session_state.page == 'Services':
    st.title("Our Services")
    st.error("### ⚠️ Important Notice: We compare electronics items only.")
    st.write("""
    - **Smart Comparison:** Compare prices between Top E-commerce sites.
    - **Real-time Data:** Get the latest current prices.
    - **Tech Focused:** Specialized only in Gadgets and Electronics.
    """)

else: # Home Page Logic (Pure Home Style)
    if query:
        st.subheader(f"Search Results for: '{query}'")
        all_products = load_manual_products()
        filtered = [p for p in all_products if query.lower() in p.get('name', '').lower()]
        
        if filtered:
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    st.image(product.get('image', ''), use_container_width=True)
                    st.markdown(f"**{product.get('name')}**")
                    st.markdown(f"#### ₹{product.get('cur_price')}")
                    st.caption(f"Site: {product.get('site_name')}")
                    st.link_button("View Deal", product.get('link'))
        else:
            st.warning("No electronics found for this search.")
    else:
        # Puran wala home page style
        st.title("Welcome to Price-Comparison System")
        st.markdown("""
        #### Track smart. Spend wise.
        Enter a product name in the search bar above to see the best electronics prices!
        
        ---
        *Manual catalog of 50+ electronics products | Powered by Streamlit*
        """)
        st.image("https://via.placeholder.com/800x300/f8f9fa/002366?text=The+Ultimate+Electronics+Comparison+Hub", use_container_width=True)
