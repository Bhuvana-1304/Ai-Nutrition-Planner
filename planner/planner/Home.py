import streamlit as st
import base64
from pathlib import Path

# ---------- Set Background Image ----------
def set_background(image_file):
    img_path = Path(__file__).parent / "images" / image_file 
    with open(img_path, "rb") as f: 
        data = f.read()
        encoded = base64.b64encode(data).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        animation: bgFade 2s ease-in forwards;
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    @keyframes bgFade {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call function with image
set_background("nutrition.jpg")

# ---------- Animated Headings ----------
st.markdown("""
    <style>
    .animated-text-container {
        position: relative;
        top: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .welcome-heading {
        font-size: 60px;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 6px black;
        opacity: 0;
        animation: fadeInSlide 2s ease-out forwards;
        animation-delay: 2s;
    }
    .subheading {
        font-size: 36px;
        font-weight: 500;
        color: white;
        margin-top: 10px;
        text-shadow: 2px 2px 6px black;
        opacity: 0;
        animation: fadeInSlideSub 2s ease-out forwards;
        animation-delay: 4s;
    }
    @keyframes fadeInSlide {
        0% {opacity: 0; transform: translateY(-30px);}
        100% {opacity: 1; transform: translateY(0);}
    }
    @keyframes fadeInSlideSub {
        0% {opacity: 0; transform: translateY(30px);}
        100% {opacity: 1; transform: translateY(0);}
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    <div class="animated-text-container">
        <div class="welcome-heading">👋 WELCOME TO NUTRIFY</div>
        <div class="subheading">🥗 Your Personal Nutritionist</div>
    </div>
""", unsafe_allow_html=True)

# ---------- Proceed Button Logic ----------
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Proceed"):
        st.session_state['show_welcome'] = True
        st.rerun()
