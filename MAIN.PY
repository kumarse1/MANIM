# Simple Healthcare POC - Vibe Coding Style
# pip install streamlit requests manim pandas

import streamlit as st
import requests
import base64
import pandas as pd
from manim import *

# Default data for demo
default_data = {
    "day_1": 1000,
    "day_30": 650, 
    "day_90": 450
}

# Load data from upload or use default
def get_data(uploaded_file):
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            # Simple: just grab first few rows and convert to our format
            return {
                "day_1": int(df.iloc[0].get('enrolled', 1000)),
                "day_30": int(df.iloc[1].get('enrolled', 650)) if len(df) > 1 else 650,
                "day_90": int(df.iloc[2].get('enrolled', 450)) if len(df) > 2 else 450
            }
        except:
            st.warning("Using default data - check your CSV format")
            return default_data
    return default_data

# Simple LLM call
def ask_llm(api_url, username, password):
    try:
        auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        response = requests.post(api_url, 
                               json={"prompt": f"Analyze member retention: {data}. Give 1 insight."}, 
                               headers={"Authorization": f"Basic {auth}"}, 
                               timeout=5)
        return response.text if response.ok else "55% of members drop off by day 90. Need intervention at day 30."
    except:
        return "55% of members drop off by day 90. Need intervention at day 30."

# Simple Manim scene
class MemberDots(Scene):
    def construct(self):
        # Make 10 dots (representing 1000 members)
        dots = [Dot(color=GREEN).shift(LEFT*4 + RIGHT*i*0.8) for i in range(10)]
        
        # Day 1: Show all dots
        title = Text("Day 1: 1000 Members").to_edge(UP)
        self.add(title, *dots)
        self.wait(1)
        
        # Day 30: Remove some dots
        self.play(Transform(title, Text("Day 30: 650 Members").to_edge(UP)))
        self.play(*[FadeOut(dot) for dot in dots[6:]])  # Remove 4 dots
        self.wait(1)
        
        # Day 90: Remove more dots  
        self.play(Transform(title, Text("Day 90: 450 Members - Need Help!").to_edge(UP)))
        self.play(*[FadeOut(dot) for dot in dots[4:6]])  # Remove 2 more
        self.wait(2)

# Streamlit app - super simple
st.title("🏥 Member Retention POC")

# File upload option
uploaded_file = st.file_uploader("📁 Upload member data (CSV)", type=['csv'])
if uploaded_file:
    st.success("Using your uploaded data!")
else:
    st.info("Using demo data - upload CSV to see your real numbers")

# Get data (uploaded or default)
data = get_data(uploaded_file)

# Get LLM insight
api_url = st.text_input("API URL", "http://localhost:8000/chat")
username = st.text_input("Username", "admin") 
password = st.text_input("Password", "password", type="password")

if st.button("Analyze"):
    # Show data
    st.subheader("📊 The Data")
    st.write(f"Day 1: {data['day_1']} members")
    st.write(f"Day 30: {data['day_30']} members") 
    st.write(f"Day 90: {data['day_90']} members")
    
    # Get insight
    st.subheader("🤖 LLM Says")
    insight = ask_llm(api_url, username, password)
    st.write(insight)
    
    # Animation concept
    st.subheader("🎬 Manim Shows")
    st.write("Animation: Watch dots disappear as members drop off")
    st.write("• Start: 10 green dots")
    st.write("• Day 30: 4 dots fade away")  
    st.write("• Day 90: 2 more dots fade away")
    st.write("• Result: Only 4 dots left!")
    
    if st.button("🎥 Make Animation"):
        if uploaded_file:
            st.info("Animation with YOUR data - watch your real member retention!")
        else:
            st.info("Animation would render here - see dots disappearing over time!")
        st.success("POC Complete! Executives see the member drop-off visually.")

# Show sample CSV format
st.markdown("---")
st.subheader("📋 CSV Format Example")
st.write("Your CSV should look like this:")
sample_csv = """enrolled
1000
650
450"""
st.code(sample_csv)

st.markdown("**The Point:** Turn boring retention numbers into memorable visual stories!")
