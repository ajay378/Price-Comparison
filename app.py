import streamlit as st
import json
import os

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Smart-Price Finder", page_icon="📈", layout="wide")

# --- UPDATED CUSTOM CSS (Behtar visuals ke liye) ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #010c1e 0%, #002b5c 100%); color: white; }
        
        /* Product Card Styling */
        .product-box {
            background: #ffffff;
            color: #1e1e1e;
            padding: 25px;
            border-radius: 18px;
            margin-bottom: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
        }
        .product-box:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.4);
            border: 1px solid #FFD700;
        }

        /* Hot Deal Badge */
        .badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #e63946;
            color: white;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
        }

        h1, h2, h3 { color: #FFD700 !important; font-family: 'Segoe UI', sans-serif; }
        .stButton>button { border-radius: 12px; font-weight: 700; text-transform: uppercase; }
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
    <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
        <h1 style="font-size: 45px; letter-spacing: 2px;">⚡ PRICE-COMPARISON PRO</h1>
        <p style="color: #FFD700; font-size: 20px;">Premium Electronics Deal Tracker</p>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'Home'

# Navigation
n1, n2, n3, n4 = st.columns([1, 1, 1, 3])
with n1: 
    if st.button("🏠 HOME"): st.session_state.page = 'Home'
with n2: 
    if st.button("🛠 SERVICES"): st.session_state.page = 'Services'
with n3: 
    if st.button("ℹ️ ABOUT US"): st.session_state.page = 'About'
with n4: 
    search_query = st.text_input("", placeholder="🔍 Search iPhone, Samsung, Laptops...", label_visibility="collapsed")

st.write("---")

# Routing Logic
if st.session_state.page == 'About':
    st.markdown('<div style="background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; border: 1px solid gold;">', unsafe_allow_html=True)
    st.title("Meet The Developers")
    st.write("Developed with ❤️ by **Team K.AJAYKUMAR**")
    st.markdown("- **K.AJAYKUMAR (Lead)**\n- **T.PRANATHI**\n- **K.SAIKEERTHANA**\n- **MD.HAROON**\n- **S.MANICHARANREDDY**")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Services':
    st.info("🚀 **Coming Soon:** Price Drop Alerts & Comparison Graphs!")

else:
    if search_query:
        all_products = load_manual_products()
        filtered = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]
        
        if filtered:
            # Stylish Result Header
            st.markdown(f"### ✨ Showing {len(filtered)} Best Deals for '{search_query}'")
            
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    # Extracting data
                    name = product.get('name', 'Product')
                    cur_p = product.get('cur_price', 0)
                    last_p = product.get('last_price', cur_p)
                    rating = product.get('rating', 0)
                    rev_count = product.get('ratingCount', 0)
                    drop = product.get('price_drop_per', 0)
                    
                    st.markdown('<div class="product-box">', unsafe_allow_html=True)
                    
                    # Hot Deal Badge
                    if drop > 40:
                        st.markdown('<span class="badge">🔥 HOT DEAL</span>', unsafe_allow_html=True)
                    
                    if product.get('image'):
                        st.image(product.get('image'), use_container_width=True)
                    
                    st.markdown(f"<h4 style='color: #222;'>{name[:45]}...</h4>", unsafe_allow_html=True)
                    
                    # Pricing Section
                    st.markdown(f"""
                        <h2 style='color: #d62828 !important; margin: 10px 0;'>₹{cur_p:,}</h2>
                        <p style='color: #38b000; font-size: 16px;'><b>{drop}% OFF</b> 
                        <span style='text-decoration: line-through; color: #999; font-size: 14px;'>₹{last_p:,}</span></p>
                    """, unsafe_allow_html=True)
                    
                    # Rating Section
                    st.markdown(f"""
                        <div style='background: #f8f9fa; padding: 5px; border-radius: 10px; margin: 10px 0;'>
                            <span style='color: #ffb703; font-size: 18px;'>★</span> <b>{rating}</b> 
                            <span style='color: #666;'>({rev_count:,} reviews)</span>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"<p style='color: #0077b6; font-weight: 600;'>🛒 {product.get('site_name')}</p>", unsafe_allow_html=True)
                    st.link_button(f"VIEW ON {product.get('site_name').upper()}", product.get('link'))
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Bhai, ye item nahi mila. Kuch aur search karke dekho!")
    else:
        # Professional Home Hero Section
        st.markdown("""
            <div style="text-align: center; padding: 50px;">
                <h1 style="font-size: 100px; margin-bottom: 0;">📦</h1>
                <h2 style="font-size: 40px;">Smartest Way to Buy Electronics</h2>
                <p style="font-size: 18px; color: #ddd;">Hazaar websites check karne ki tension khatam! <br> Best prices, ratings, aur real-time deals yahan milegi.</p>
                <div style="margin-top: 30px; padding: 15px; border-top: 2px solid #FFD700; display: inline-block;">
                    <b>Currently Tracking: 50+ Premium Tech Products</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align: center; color: #888;'>© 2026 | Developed for Samsung Innovation Campus Project</p>", unsafe_allow_html=True)
