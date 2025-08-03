import streamlit as st
from PIL import Image

# Redirect if accessed directly without coming from Home page
if not st.session_state.get("show_welcome"):
    st.warning("Please click 'Proceed' on the Home page to continue.")
    st.stop()

# Page setup
st.set_page_config(page_title="Welcome to Nutrify", layout="wide")

# CSS styling
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: 700;
            text-align: center;
            color: #ffffff;
        }
        .sub-title {
            font-size: 24px;
            text-align: center;
            color: #cccccc;
            margin-bottom: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Headings
st.markdown('<div class="main-title">YOUR PERSONAL SPACE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Live Healthy</div>', unsafe_allow_html=True)

st.markdown("---")

# Columns for image and form
col1, col2 = st.columns([1, 1])

# Image on the left
with col1:
    try:
        img = Image.open("images/welcome_banner.jpg")
        st.image(img, width=250)
    except:
        st.warning("Welcome image not found at `images/welcome_banner.jpg`.")

# Name and Email on the right
with col2:
    st.subheader("Let's Get Started 📝")
    name = st.text_input("Enter your Name")
    email = st.text_input("Enter your Email")

    if st.button("👉 Let's Plan My Diet"):
        if name and email:
            st.session_state["name"] = name
            st.session_state["email"] = email
            st.success("Redirecting to Diet Planner...")
            st.switch_page("pages/2_Diet_Planner.py")  # make sure this file exists
        else:
            st.warning("Please fill in both fields to continue.")
