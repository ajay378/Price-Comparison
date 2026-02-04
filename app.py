import streamlit as st
import json
import os
import jinja2

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- CSS: BACKGROUND & STYLING ---
st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background: linear-gradient(rgba(0, 35, 102, 0.9), rgba(0, 35, 102, 0.9)), 
                        url("https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }

        /* Hide Sidebar & Header */
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Highlight Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3.5em;
            background-color: #FFD700;
            color: #002366;
            border: none;
            font-weight: 900;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #ffffff;
            color: #002366;
            transform: scale(1.05);
        }

        /* Content Cards */
        .content-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-top: 20px;
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

# --- TOP NAVIGATION BAR ---
NAV_HTML = """
<div style="background-color: rgba(0, 35, 102, 0.8); padding: 20px 50px; display: flex; align-items: center; border-radius: 15px; margin-bottom: 25px; border: 1px solid #FFD700;">
    <div style="background: #FFD700; color: #002366; padding: 8px 15px; border-radius: 8px; font-weight: 900; margin-right: 20px; font-size: 24px;">PCS</div>
    <span style="font-size: 28px; font-weight: 700; color: white; letter-spacing: 1px;">Price-Comparison System</span>
</div>
"""
st.components.v1.html(NAV_HTML, height=100)

# --- NAVIGATION LOGIC ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    if st.button("🏠 HOME"): st.session_state.page = 'Home'
with col2:
    if st.button("🛠 SERVICES"): st.session_state.page = 'Services'
with col3:
    if st.button("ℹ️ ABOUT US"): st.session_state.page = 'About'
with col4:
    query = st.text_input("", placeholder="Search for Laptops, Phones, Gadgets...", label_visibility="collapsed")

# --- PAGE CONTENT ---

if st.session_state.page == 'About':
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.title("Team Behind The Project")
    st.markdown("""
    ### Developed By:
    1. **Ajay Konda**
    2. **Pranati**
    3. **Sai Keerthana**
    4. **Haroon**
    5. **Mani Charan**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Services':
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.title("Our Specialized Services")
    st.error("### ⚠️ Policy: We compare electronics items only.")
    st.write("We scan multiple e-commerce platforms to bring you the best prices for high-end tech gadgets and electronics.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    if query:
        all_products = load_manual_products()
        filtered = [p for p in all_products if query.lower() in p.get('name', '').lower()]
        if filtered:
            st.subheader(f"Results for '{query}'")
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    st.markdown('<div style="background: white; color: black; padding: 15px; border-radius: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
                    st.image(product.get('image', ''), use_container_width=True)
                    st.write(f"**{product.get('name')}**")
                    st.markdown(f"<h3 style='color: #e63946;'>₹{product.get('cur_price')}</h3>", unsafe_allow_html=True)
                    st.link_button(f"Buy on {product.get('site_name')}", product.get('link'))
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No electronics found for this search.")
    else:
        # HOME PAGE WITH IMAGE
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.title("Welcome to Price-Comparison System")
        st.write("### Track smart. Spend wise.")
        
        # Professional Tech Image
        st.image("https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", 
                 caption="Find the best deals on latest electronics", use_container_width=True)
        
        st.markdown("""
        <p style='text-align: center; font-size: 18px; margin-top: 20px;'>
            Your one-stop destination to compare prices of iPhones, Laptops, and other premium gadgets.
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
