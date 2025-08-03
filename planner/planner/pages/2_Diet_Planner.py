import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("nutrify_expanded_dataset.csv")

# Page setup
st.set_page_config(page_title="Nutrify - Personalized Diet Planner")
st.title("🌱 Nutrify - Your Personalized Diet Planner")

# Sidebar user input
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Age", min_value=1, max_value=100)
weight = st.sidebar.number_input("Weight (kg)", min_value=1, max_value=200)
height_cm = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

# Period condition for females
on_period = None
if gender == "Female":
    on_period = st.sidebar.radio("Are you on your period?", ["Yes", "No"])

diet_type = st.sidebar.radio("Diet Preference", ["Veg", "Non-Veg", "Both"])

# Allergy selection
allergy = st.sidebar.multiselect("Allergies", [
    "None", "Egg", "Dairy", "Gluten", "Nuts", "Soy", "Fish", "Shellfish", "Chia", "Corn",
    "Peanuts", "Wheat", "Lactose", "Sesame", "Mustard", "Celery", "Mushrooms", "Tomato", "Citrus", "Banana",
    "Pineapple", "Chocolate", "Caffeine", "Strawberries", "Artificial Sweeteners", "Preservatives",
    "MSG", "Food Colorants", "Sulfites", "Tartrazine", "Oats", "Beetroot", "Spinach", "Apple", "Coconut",
    "Honey", "Avocado", "Kiwi", "Watermelon", "Mango", "Raspberries", "Blueberries", "Grapes",
    "Carrot", "Peas", "Lentils", "Cashew", "Walnuts", "Almonds"
])

# Health conditions
diseases = st.sidebar.multiselect("Health Conditions", [
    "None", "Diabetes", "High BP", "Thyroid", "Cholesterol", "Obesity", "PCOD", "Anemia",
    "IBS", "Celiac Disease", "Gastritis", "Kidney Disease", "Heart Disease", "Liver Disease",
    "Arthritis", "Osteoporosis", "Gout", "Cancer", "Asthma", "Migraine", "Acid Reflux", "Hypertension",
    "Vitamin D Deficiency", "Iron Deficiency", "Hypothyroidism", "Hyperthyroidism", "Piles", "Jaundice",
    "Hepatitis", "Gallbladder Stones", "Constipation", "UTI", "Menstrual Cramps", "Endometriosis", "Vertigo",
    "Acne", "Eczema", "Psoriasis", "Dandruff", "Hair Fall", "Sleep Apnea", "Insomnia", "Depression",
    "Anxiety", "ADHD", "Parkinson's", "Alzheimer's", "Sinusitis", "Tonsillitis"
])

# Show motivational images
if not st.session_state.get("show_result", False):
    st.markdown("<h4 style='text-align: center;'>🍴👩🏼‍⚕️ STAY HEALTHY STAY HAPPY</h4>", unsafe_allow_html=True)
    cols = st.columns(4)
    image_paths = [
        "images/image2.jpg",
        "images/image1.jpg",
        "images/image4.jpg",
        "images/image3.jpg"
    ]
    for i, col in enumerate(cols):
        with col:
            try:
                col.image(image_paths[i], width=160)
            except:
                col.error("Image not found!")

# Generate Diet Plan Button
if st.button("Generate Diet Plan"):
    st.session_state['generate_clicked'] = True

    st.subheader("📊 BMI and Weight Suggestion")
    if height_cm > 0:
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        st.write(f"**Your BMI is:** {bmi:.2f}")

        if bmi < 18.5:
            st.info("You are underweight. Consider a healthy weight-gain diet. 🍽️")
        elif 18.5 <= bmi <= 24.9:
            st.success("Your weight is normal. Maintain a balanced diet! ✅")
        elif 25 <= bmi <= 29.9:
            st.warning("You are overweight. A weight-loss friendly plan is recommended. ⚠️")
        else:
            st.error("You are in the obese category. Please consult a doctor for personalized advice. 🚨")
    else:
        st.warning("Please enter a valid height to calculate BMI.")

    st.subheader("🍽️ Your Personalized Diet Plan")

    # Filter by diet type
    if diet_type != "Both":
        filtered_df = df[df['Category'] == diet_type].copy()
    else:
        filtered_df = df.copy()

    # Filter for period
    if gender == "Female" and on_period == "Yes":
        filtered_df = filtered_df[filtered_df['Period_Friendly'] == 1]

    # Filter diseases
    disease_column_map = {
        "Diabetes": "Diabetes_Friendly",
        "High BP": "High_BP_Friendly"
    }
    for d in diseases:
        if d != "None" and disease_column_map.get(d) in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[disease_column_map[d]] == 1]

    # Filter allergies
    filtered_df['Allergens'] = filtered_df['Allergens'].fillna("").astype(str)
    for a in allergy:
        if a != "None":
            filtered_df = filtered_df[~filtered_df['Allergens'].str.contains(a, case=False, na=False)]

    # Smart meal selection
    def get_unique_meals(meal_type, used_items, count=4):
        options = filtered_df[filtered_df['Meal_Type'] == meal_type]['Food_Item'].unique().tolist()
        options = list(set(options) - used_items)
        random.shuffle(options)
        selection = options[:count] if options else ["No suitable options"]
        used_items.update(selection)
        return selection

    used_items = set()
    meal_types = ["Breakfast", "Lunch", "Snack", "Dinner"]
    meal_icons = {
        "Breakfast": "🥣",
        "Lunch": "🍛",
        "Snack": "🥗",
        "Dinner": "🍽️"
    }

    for meal in meal_types:
        icon = meal_icons.get(meal, "")
        st.markdown(f"""
        <div style='
            background: #ffffff11;
            padding: 16px;
            border-radius: 16px;
            margin: 20px 0;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease forwards;
            backdrop-filter: blur(4px);
            border: 1px solid #ffffff33;
        '>
            <h3 style='color:#fff'>{icon} {meal} Options</h3>
        </div>
        """, unsafe_allow_html=True)

        items = get_unique_meals(meal, used_items, count=4)
        for food in items:
            st.markdown(f"<p style='color:white; margin-left: 20px;'>• {food}</p>", unsafe_allow_html=True)

    # Plotly Nutrient Breakdown (sample static data)
    nutrients = {
        "Protein": 60,
        "Carbs": 220,
        "Fat": 70
    }
    st.subheader("📊 Nutrient Breakdown")
    fig = go.Figure(data=[go.Pie(
        labels=list(nutrients.keys()),
        values=list(nutrients.values()),
        hole=0.4
    )])
    fig.update_layout(title_text="Daily Nutrient Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Animation styling
    st.markdown("""
        <style>
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    st.success("Stay healthy with your custom diet plan! 💪")
