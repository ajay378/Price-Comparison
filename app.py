import streamlit as st
import json
import os

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- IMPROVED CSS FOR VISIBILITY ---
st.markdown("""
    <style>
        /* Dark Background */
        .stApp { 
            background: linear-gradient(135deg, #001f3f 0%, #003366 100%); 
            color: #ffffff; 
        }
        
        /* Product Card - High Contrast Text */
        .product-box {
            background: #ffffff;
            color: #1a1a1a; /* Dark text for white background */
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            border: 1px solid rgba(0,0,0,0.1);
        }
        
        .product-box p, .product-box h4, .product-box span {
            color: #1a1a1a !important; /* Force black text inside cards */
        }

        /* Navigation Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #FFD700;
            color: #001f3f;
            border: none;
            font-weight: bold;
            font-size: 16px;
        }

        h1, h2, h3 { color: #FFD700 !important; }
        
        /* Badge Styling */
        .badge {
            background: #d62828;
            color: white !important;
            padding: 4px 12px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
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
    <div style="background: rgba(255,215,0,0.1); padding: 25px; border-radius: 15px; border-left: 10px solid #FFD700; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 35px;">📊 Price-Comparison System</h1>
        <p style="margin:0; color: #eeeeee;">Unified platform for premium electronics price tracking</p>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'Home'

# --- NAVIGATION ---
n1, n2, n3, n4 = st.columns([1, 1, 1, 3])
with n1: 
    if st.button("HOME"): st.session_state.page = 'Home'
with n2: 
    if st.button("SERVICES"): st.session_state.page = 'Services'
with n3: 
    if st.button("ABOUT US"): st.session_state.page = 'About'
with n4: 
    search_query = st.text_input("", placeholder="🔍 Search Products (iPhone, Laptop, Watch...)", label_visibility="collapsed")

st.write("---")

# --- PAGES (Only English Content) ---
if st.session_state.page == 'About':
    st.markdown('<div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">', unsafe_allow_html=True)
    st.title("About the Developers")
    st.markdown("""
    ### Project Development Team:
    1. **K.AJAYKUMAR (TL)**
    2. **T.PRANATHI**
    3. **K.SAIKEERTHANA**
    4. **MD.HAROON**
    5. **S.MANICHARANREDDY**
    
    **Project Objective:** To simplify the electronics shopping experience by providing real-time price comparisons across major e-commerce platforms.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Services':
    st.markdown('<div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px;">', unsafe_allow_html=True)
    st.title("Our Specialized Services")
    st.markdown("""
    * **Price Tracking:** Monitor live price changes for premium gadgets.
    * **Platform Comparison:** Compare deals from Amazon, Flipkart, and more.
    * **User Analytics:** Data-driven insights on product ratings and reviews.
    * **Verified Links:** Direct access to official retailer product pages.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    if search_query:
        all_products = load_manual_products()
        filtered = [p for p in all_products if search_query.lower() in p.get('name', '').lower()]
        
        if filtered:
            st.subheader(f"Search Results: {len(filtered)} items found")
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    # Extract Data
                    cur_p = product.get('cur_price', 0)
                    last_p = product.get('last_price', cur_p)
                    rating = product.get('rating', 'N/A')
                    rev_count = product.get('ratingCount', 0)
                    drop = product.get('price_drop_per', 0)
                    
                    st.markdown('<div class="product-box">', unsafe_allow_html=True)
                    
                    # High Discount Badge
                    if drop > 40:
                        st.markdown('<span class="badge">TOP DEAL</span>', unsafe_allow_html=True)
                    
                    if product.get('image'):
                        st.image(product.get('image'), use_container_width=True)
                    
                    # Title
                    st.markdown(f"<h4 style='font-size: 16px; margin: 10px 0;'>{product.get('name')[:60]}...</h4>", unsafe_allow_html=True)
                    
                    # Prices
                    st.markdown(f"<h2 style='color: #d62828 !important; margin: 0;'>₹{cur_p:,}</h2>", unsafe_allow_html=True)
                    if drop > 0:
                        st.markdown(f"<p style='color: #2b9348; font-size: 14px; margin: 0;'><b>{drop}% OFF</b> <span style='text-decoration: line-through; color: #777;'>₹{last_p:,}</span></p>", unsafe_allow_html=True)
                    
                    # Rating/Review
                    st.markdown(f"<p style='font-size: 14px; margin-top: 8px;'>⭐ {rating} | 👥 {rev_count:,} Reviews</p>", unsafe_allow_html=True)

                    st.markdown(f"<p style='color: #0077b6; font-size: 12px; font-weight: bold;'>Retailer: {product.get('site_name')}</p>", unsafe_allow_html=True)
                    st.link_button(f"VISIT {product.get('site_name').upper()}", product.get('link'))
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No electronic items match your search. Please try keywords like 'Samsung' or 'iPhone'.")
    else:
        # HOME PAGE (Pure English)
        st.markdown('<div style="text-align: center; padding: 50px;">', unsafe_allow_html=True)
        st.title("Welcome to Price-Comparison System")
        st.write("### Smart Tracking. Better Savings.")
        st.markdown("<h1 style='font-size: 100px;'>🛒📱💻</h1>", unsafe_allow_html=True)
        st.write("Access current market prices for 50+ verified electronics items instantly.")
        st.info("💡 **Instructions:** Use the search bar above to find the best deals on smartphones, laptops, and more.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #bbbbbb; padding: 20px;'>© 2026 Price-Comparison System | Samsung Innovation Campus Project</p>", unsafe_allow_html=True)
