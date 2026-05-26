import streamlit as st
import datetime
import random
from core.graph import create_travel_graph

# 1. Page Configuration & Aesthetic CSS
st.set_page_config(page_title="My Travel Planner", page_icon="✈️", layout="wide")

# Custom CSS for Background Image and Professional Styling
# Custom CSS for Background Image, Dark Glassmorphism, and Professional Styling
st.markdown("""
    <style>
    /* 1. Full Page Background Image */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    
    /* 2. Full-Page Dark Frosted Glass Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.65) !important; /* Dark tint */
        backdrop-filter: blur(15px) !important; /* Heavy blur */
        -webkit-backdrop-filter: blur(15px) !important; /* Safari support */
        z-index: 0;
    }

    /* 3. Bring content above the glass overlay */
    .main {
        position: relative;
        z-index: 1;
    }

    /* 4. Make Streamlit's default header transparent */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 5. Remove the inner card background so it blends seamlessly */
    [data-testid="stMainBlockContainer"], .block-container {
        background-color: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        border: none !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding-top: 2rem !important; /* Pulls the title up to reduce the gap */
        padding-bottom: 2rem !important;
    }

    /* 6. Force all text to be crisp white */
    h1, h2, h3, p, label, li, span, div {
        color: #ffffff !important;
    }

    /* 7. Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        transform: translateY(-2px);
    }

    /* 8. Destination Card Styling & Uniform Images */
    [data-testid="stImage"] img {
        height: 200px !important;
        object-fit: cover !important;
        border-radius: 15px 15px 0 0 !important;
    }
    .stButton>button {
        border-radius: 0 0 10px 10px !important;
        margin-top: -15px !important; 
    }
    button[kind="primary"] {
        margin-top: 28px !important; /* Pushes it exactly down to match the input labels */
        border-radius: 10px !important; /* Restores all rounded corners */
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic to Trigger LangGraph
def generate_plan(origin, destination, start_date, end_date):
    with st.spinner(f"Agents are coordinating your trip to {destination}..."):
        app = create_travel_graph()
        inputs = {
            "origin": origin,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
        result = app.invoke(inputs)
        return result.get("total_cost_estimate", "Error generating itinerary.")

# 3. Header Section
st.title("My Travel Planner")
st.write("AI-Powered Multi-Agent System for Modern Travelers")

# 4. Search Bar Section (Horizontal Layout)
col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 1.5, 1.5])

with col1:
    origin_input = st.text_input("Origin", value="JFK", placeholder="City or Airport Code")
with col2:
    dest_input = st.text_input("Destination", placeholder="Where to?")
with col3:
    s_date = st.date_input("Start Date", datetime.date.today())
with col4:
    e_date = st.date_input("End Date", datetime.date.today() + datetime.timedelta(days=7))
with col5:
    # Removed the st.write(" ") padding
    if st.button("Generate Itinerary", type="primary"):
        if dest_input:
            output = generate_plan(origin_input, dest_input, s_date, e_date)
            st.session_state['itinerary'] = output
        else:
            st.error("Please enter a destination.")

# Display Results
if 'itinerary' in st.session_state:
    st.markdown("---")
    st.subheader(f" Planned Trip to {dest_input if dest_input else 'Destination'}")
    st.markdown(st.session_state['itinerary'])

# 5. Popular Destinations Section
st.markdown("---")
st.header(" Some Popular Travel Destinations")

# 12 Popular Destinations Data
popular_dests = [
    {"name": "Santorini, Greece", "img": "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?auto=format&fit=crop&w=600&q=80"},
    {"name": "Kyoto, Japan", "img": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=600&q=80"},
    {"name": "Bali, Indonesia", "img": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=600&q=80"},
    {"name": "Swiss Alps, Switzerland", "img": "https://images.unsplash.com/photo-1531310197839-ccf54634509e?auto=format&fit=crop&w=600&q=80"},
    {"name": "Paris, France", "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=600&q=80"},
    {"name": "Maldives", "img": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=600&q=80"},
    {"name": "Machu Picchu, Peru", "img": "https://images.unsplash.com/photo-1526392060635-9d6019884377?auto=format&fit=crop&w=600&q=80"},
    {"name": "Amalfi Coast, Italy", "img": "https://images.unsplash.com/photo-1612698093158-e07ac200d44e?auto=format&fit=crop&w=600&q=80"},
    {"name": "Bora Bora, French Polynesia", "img": "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=600&q=80"},
    {"name": "Reykjavik, Iceland", "img": "https://images.unsplash.com/photo-1517411032315-54ef2cb783bb?auto=format&fit=crop&w=600&q=80"},
    {"name": "New York, USA", "img": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=600&q=80"},
    {"name": "Cape Town, South Africa", "img": "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?auto=format&fit=crop&w=600&q=80"},
]

# Display 12 Cards in a 4-column grid
rows = [popular_dests[i:i + 4] for i in range(0, len(popular_dests), 4)]

for row in rows:
    cols = st.columns(4)
    for i, dest in enumerate(row):
        with cols[i]:
            st.image(dest['img'], width='stretch')
            if st.button(f"Plan for {dest['name']}", key=dest['name']):
                # When a card is clicked, we trigger the LangGraph with random dates
                random_days = random.randint(5, 10)
                start = datetime.date.today() + datetime.timedelta(days=random.randint(30, 60))
                end = start + datetime.timedelta(days=random_days)
                
                output = generate_plan(origin_input, dest['name'], start, end)
                st.session_state['itinerary'] = output
                st.rerun()