
import streamlit as st
import pandas as pd
import random
from pathlib import Path

# Load dataset
APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR.parent / "nutrify_expanded_dataset.csv"
df = pd.read_csv(DATA_PATH)
# Page setup
st.set_page_config(page_title="Nutrify - Personalized Diet Planner")
st.title("🌱 Nutrify - Your Personalized Diet Planner")

# Sidebar user input
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Age", min_value=1, max_value=100)
weight = st.sidebar.number_input("Weight (kg)", min_value=1, max_value=200)
height_cm = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

# Show period question only if gender is Female
on_period = None
if gender == "Female":
    on_period = st.sidebar.radio("Are you on your period?", ["Yes", "No"])

diet_type = st.sidebar.radio("Diet Preference", ["Veg", "Non-Veg", "Both"])

# Allergy and disease options
allergy = st.sidebar.multiselect("Allergies", [
    "None", "Egg", "Dairy", "Gluten", "Nuts", "Soy", "Fish", "Shellfish", "Chia", "Corn",
    "Peanuts", "Wheat", "Lactose", "Sesame", "Mustard", "Celery", "Mushrooms", "Tomato", "Citrus", "Banana",
    "Pineapple", "Chocolate", "Caffeine", "Strawberries", "Artificial Sweeteners", "Preservatives",
    "MSG", "Food Colorants", "Sulfites", "Tartrazine", "Oats", "Beetroot", "Spinach", "Apple", "Coconut",
    "Honey", "Avocado", "Kiwi", "Watermelon", "Mango", "Raspberries", "Blueberries", "Grapes",
    "Carrot", "Peas", "Lentils", "Cashew", "Walnuts", "Almonds"
])

diseases = st.sidebar.multiselect("Health Conditions", [
    "None", "Diabetes", "High BP", "Thyroid", "Cholesterol", "Obesity", "PCOD", "Anemia",
    "IBS", "Celiac Disease", "Gastritis", "Kidney Disease", "Heart Disease", "Liver Disease",
    "Arthritis", "Osteoporosis", "Gout", "Cancer", "Asthma", "Migraine", "Acid Reflux", "Hypertension",
    "Vitamin D Deficiency", "Iron Deficiency", "Hypothyroidism", "Hyperthyroidism", "Piles", "Jaundice",
    "Hepatitis", "Gallbladder Stones", "Constipation", "UTI", "Menstrual Cramps", "Endometriosis", "Vertigo",
    "Acne", "Eczema", "Psoriasis", "Dandruff", "Hair Fall", "Sleep Apnea", "Insomnia", "Depression",
    "Anxiety", "ADHD", "Parkinson's", "Alzheimer's", "Sinusitis", "Tonsillitis"
])

salads = ["Cucumber Salad", "Carrot Raita", "Sprouts Salad", "Tomato Onion Salad", "Mint Curd Salad"]
seeds = ["Sunflower Seeds", "Flaxseeds", "Pumpkin Seeds", "Chia Seeds", "Sesame Seeds"]
fruits = ["Apple", "Banana", "Papaya", "Guava", "Orange", "Pomegranate", "Watermelon"]

if st.sidebar.button("Generate Diet Plan"):
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

    if diet_type == "Both":
        filtered_df = df.copy()
    else:
        filtered_df = df[df['Category'] == diet_type]

    if gender == "Female" and on_period == "Yes":
        filtered_df = filtered_df[filtered_df['Period_Friendly'] == 1]

    disease_column_map = {
        d: d.replace(" ", "_").replace("'", "").replace("-", "").replace(".", "").replace(",", "") + "_Friendly"
        for d in diseases if d != "None"
    }
    for disease, col in disease_column_map.items():
        if col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col] == 1]

    for a in allergy:
        if a != "None":
            filtered_df = filtered_df[~filtered_df['Allergens'].astype(str).str.contains(a, na=False)]

    def get_unique_meals(meal_type):
        return filtered_df[filtered_df['Meal_Type'] == meal_type]['Food_Item'].dropna().unique().tolist()

    breakfast_items = get_unique_meals("Breakfast")
    lunch_items = get_unique_meals("Lunch")
    snack_items = get_unique_meals("Snack")
    dinner_items = get_unique_meals("Dinner")

    random.shuffle(breakfast_items)
    random.shuffle(lunch_items)
    random.shuffle(snack_items)
    random.shuffle(dinner_items)

    breakfast_main = random.sample(breakfast_items, min(2, len(breakfast_items)))
    breakfast_salad = [random.choice(salads)]
    breakfast_seed = [random.choice(seeds)]
    fruit1 = random.choice(fruits)
    breakfast = breakfast_main + breakfast_salad + breakfast_seed + [fruit1]

    lunch = random.sample(lunch_items, min(4, len(lunch_items)))
    rice_used = any("rice" in item.lower() or "chawal" in item.lower() for item in lunch)
    roti_used = any("roti" in item.lower() for item in lunch)

    if roti_used:
        snack_pool = [s for s in snack_items if "roti" not in s.lower()]
    else:
        snack_pool = snack_items
    snack = random.sample(snack_pool, min(4, len(snack_pool)))

    dinner_pool = [d for d in dinner_items if (not rice_used or "rice" not in d.lower()) and (not roti_used or "roti" not in d.lower())]
    dinner_main = random.sample(dinner_pool, min(3, len(dinner_pool))) if len(dinner_pool) >= 3 else ["Light Soup"]
    fruit2 = random.choice([f for f in fruits if f != fruit1])
    dinner = dinner_main + [fruit2]

    st.write("**Breakfast:**")
    for item in breakfast:
        st.markdown(f"- {item}")
        

    st.write("**Lunch:**")
    for item in lunch:
        st.markdown(f"- {item}")

    st.write("**Snack:**")
    for item in snack:
        st.markdown(f"- {item}")

    st.write("**Dinner:**")
    for item in dinner:
        st.markdown(f"- {item}")

    st.success("Stay healthy with your custom diet plan! 💪")
