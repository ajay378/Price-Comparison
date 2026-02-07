import streamlit as st
import json
import os
from datetime import datetime

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Price-Comparison System", page_icon="📊", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #001f3f 0%, #003366 100%); color: white; }
        [data-testid="stSidebar"] {display: none;}
        .product-box {
            background: white; color: #333; padding: 20px;
            border-radius: 15px; margin-bottom: 20px;
            text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            min-height: 520px; /* Sab elements fit hone ke liye height badhayi hai */
            display: flex; flex-direction: column; justify-content: space-between;
        }
        h1, h2, h3 { color: #FFD700 !important; }
        .stButton>button {
            background-color: #FFD700; color: #001f3f; font-weight: 800;
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
    search_query = st.text_input("",
