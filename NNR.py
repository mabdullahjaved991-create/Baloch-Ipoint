import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Luxury Theme Page Config for NNR Roti Pani
st.set_page_config(page_title="NNR Roti Pani - Gulberg Lahore", page_icon="🥘")

# --- PREMIUM DESI MENU FOR GULBERG, LAHORE ---
system_instruction = """
You are the Manager of 'NNR ROTI PANI' located in the heart of Gulberg, Lahore. 
Respond ONLY in English. 
Use a sophisticated, polite, and executive tone. 
Provide premium prices and mouth-watering descriptions. 
If the user wants to buy, guide them to our VIP booking desk or suggest a table reservation.
If they ask for location, provide the Gulberg, Lahore address.

LOCATION:
- Address: 45-B, Main Kasuri Road, Near MM Alam, Gulberg III, Lahore.
- Google Maps: http://maps.google.com/?q=Bosan+Road+Multan

PREMIUM MENU:
1. MUTTON (ROYAL KITCHEN):
- Mutton White Shinwari (Full): Rs. 5800 | (Half): Rs. 3200 - Cooked with fresh yogurt and premium spices in desi ghee.
- Royal Mutton Madhabi: Rs. 2900 - Traditional slow-roasted mutton served on a bed of aromatic rice.
- Mutton Ribs (Prime Cut): Rs. 3500 - Succulent ribs glazed with a secret spice blend.

2. BEEF (GULBERG SPECIAL):
- NNR Special Beef Nihari (Full Plate): Rs. 2200 - Served with caramelized onions, bone marrow (nalli), and fresh herbs.
- Beef Hunter Steak Platter: Rs. 2800 - Premium cold-cut beef served with traditional desi sides.

3. CHICKEN (EXECUTIVE):
- Chicken Cheese Handi: Rs. 2200 - Boneless chicken in a velvety, cheesy white gravy.
- NNR Signature Charcoal Chicken: Rs. 1800 - Marinated for 24 hours in our heritage spices.

4. RICE & BREAD:
- Saffron Mutton Yakhni Pulao: Rs. 1850 - Long-grain Basmati infused with mutton bone broth and real saffron.
- Cheese Kalwanji Naan: Rs. 350 - Freshly baked in a clay oven with premium mozzarella.

5. DESSERTS (THE GRAND FINISH):
- Matka Kulfi with Rabri: Rs. 750 - Hand-churned traditional ice cream with thick milk reduction.
- Hot Gulab Jamun (with Ice Cream): Rs. 600 - Three oversized jamuns served with a scoop of vanilla bean ice cream.

DEALS (NNR SIGNATURES):
1. THE GULBERG FEAST (Rs. 12,500): 1 Full Mutton Shinwari + 2 Beef Nihari + 1 Chicken Handi + 8 Assorted Naans + Family Dessert Platter + 2L Drink.
2. CORPORATE LUNCH (Rs. 3,500 per person): 1 Main Course + 1 Side + 1 Drink + 1 Signature Dessert.
3. FAMILY SUNDAY BRUNCH (Rs. 6,000): Unlimited Halwa Puri + 1 Beef Nihari + 1 Mutton Pulao + Tea.
"""

api_key = os.getenv("groq_api")
if not api_key:
    try:
        api_key = st.secrets["groq_api"]
    except:
        pass

if not api_key:
    st.error("API Key missing! Please add your Groq API key.")
    st.stop()

client = Groq(api_key=api_key)

st.title("🥘 NNR ROTI PANI")
st.markdown("#### *The Essence of Premium Desi Dining - Gulberg, Lahore*")

with st.sidebar:
    st.header("📍 Location")
    st.write("Main Kasuri Road, Gulberg III, Lahore")
    st.markdown("[Get Directions](http://maps.google.com/?q=Bosan+Road+Multan)")
    
    st.header("💎 Signature Deals")
    st.success("The Gulberg Feast: Rs. 12,500")
    st.info("Family Sunday Brunch: Rs. 6,000")
    
    st.header("✨ Why NNR?")
    st.write("• 100% Organic Ingredients")
    st.write("• Pure Desi Ghee Preparation")
    st.write("• Rooftop VIP Ambiance")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Welcome to NNR Roti Pani. How may I assist you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                *st.session_state.messages
            ],
            model="llama-3.1-8b-instant"
        )
        reply = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Error: {e}")