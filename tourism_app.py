
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
page_title="Wanderly India",
page_icon="🌍",
layout="wide",
initial_sidebar_state="expanded"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {font-family:'Poppins',sans-serif;}
.stApp {
background: linear-gradient(135deg,#fff7ed,#e0f2fe,#ecfdf5);
background-size: 300% 300%;
animation:bg 14s ease infinite;
}
@keyframes bg {
0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}
}
.hero {
padding:55px 40px;
border-radius:28px;
color:white;
background:
linear-gradient(90deg,rgba(2,6,23,.82),rgba(2,6,23,.30)),
url("https://images.unsplash.com/photo-1524492412937-b28074a5d7da");
background-size:cover;
background-position:center;
box-shadow:0 20px 50px rgba(15,23,42,.25);
}
.hero h1 {font-size:54px;font-weight:800;margin:0;}
.hero p {font-size:19px;}
.card {
background:rgba(255,255,255,.72);
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,.8);
border-radius:22px;
padding:20px;
margin-bottom:15px;
box-shadow:0 10px 30px rgba(15,23,42,.10);
transition:.3s;
}
.card:hover {transform:translateY(-6px);box-shadow:0 18px 35px rgba(15,23,42,.18);}
.price {font-size:27px;font-weight:800;color:#0f766e;}
.badge {
display:inline-block;padding:6px 12px;border-radius:999px;
background:#ffedd5;color:#c2410c;font-weight:600;
}
.section {font-size:30px;font-weight:800;color:#0f172a;margin:30px 0 15px;}
.small {color:#64748b;}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
places = {
"Goa": {
"state":"Goa",
"lat":15.2993, "lon":74.1240,
"image":"https://images.unsplash.com/photo-1512343879784-a960bf40e7f2",
"desc":"Beaches, nightlife, water sports and relaxing resorts.",
"price":12999
},
"Kashmir": {
"state":"Jammu & Kashmir",
"lat":34.0837, "lon":74.7973,
"image":"https://images.unsplash.com/photo-1600185365483-26d7a4cc7519",
"desc":"Mountains, lakes, gardens and unforgettable valley views.",
"price":24999
},
"Jaipur": {
"state":"Rajasthan",
"lat":26.9124, "lon":75.7873,
"image":"https://images.unsplash.com/photo-1599661046289-e31897846e41",
"desc":"Forts, palaces, markets and royal Rajasthani culture.",
"price":18999
},
"Kerala": {
"state":"Kerala",
"lat":9.9312, "lon":76.2673,
"image":"https://images.unsplash.com/photo-1602216056096-3b40cc0c9944",
"desc":"Backwaters, greenery, beaches and peaceful houseboats.",
"price":16999
},
"Manali": {
"state":"Himachal Pradesh",
"lat":32.2432, "lon":77.1892,
"image":"https://images.unsplash.com/photo-1626621341517-bbf3d9990a23",
"desc":"Snowy mountains, valleys, trekking and adventure.",
"price":21999
},
"Agra": {
"state":"Uttar Pradesh",
"lat":27.1767, "lon":78.0081,
"image":"https://images.unsplash.com/photo-1564507592333-c60657eea523",
"desc":"Explore the Taj Mahal and fascinating Mughal history.",
"price":9999
}
}

if "wishlist" not in st.session_state:
st.session_state.wishlist = []
if "reviews" not in st.session_state:
st.session_state.reviews = []
if "bookings" not in st.session_state:
st.session_state.bookings = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 Wanderly India")
page = st.sidebar.radio(
"Navigation",
["🏠 Home","🗺️ Explore Map","☀️ Weather","✈️ Trip Planner",
"❤️ Wishlist","⭐ Reviews","🎫 Booking"]
)

st.sidebar.markdown("---")
st.sidebar.info("Plan • Explore • Book • Remember ✨")

# ---------------- HOME ----------------
if page == "🏠 Home":
st.markdown("""
<div class="hero">
<h1>Explore India 🌈</h1>
<p>Discover beaches, mountains, royal cities and unforgettable adventures.</p>
<span class="badge">✈️ Your journey starts here</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">🔥 Popular Destinations</div>', unsafe_allow_html=True)

search = st.text_input("🔎 Search a destination", placeholder="Goa, Kashmir, Jaipur...")

selected = [
(name, data) for name, data in places.items()
if not search or search.lower() in name.lower()
]

cols = st.columns(3)
for i, (name, data) in enumerate(selected):
with cols[i % 3]:
    st.markdown(f"""
    <div class="card">
        <img src="{data['image']}" style="width:100%;height:190px;object-fit:cover;border-radius:16px;">
        <h3>{name} 📍</h3>
        <p class="small">{data['state']}</p>
        <p>{data['desc']}</p>
        <p class="price">₹{data['price']:,}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"❤️ {name}", key=f"wish_{name}"):
        if name not in st.session_state.wishlist:
            st.session_state.wishlist.append(name)
            st.success(f"{name} added to wishlist!")

# ---------------- MAP ----------------
elif page == "🗺️ Explore Map":
st.markdown('<div class="section">🗺️ Interactive Destination Map</div>', unsafe_allow_html=True)

destination = st.selectbox("Choose destination", list(places.keys()))
d = places[destination]

map_df = pd.DataFrame({
"lat":[d["lat"]],
"lon":[d["lon"]]
})
st.map(map_df, zoom=6)

st.markdown(f"""
<div class="card">
<h2>📍 {destination}</h2>
<p>{d['desc']}</p>
<p><b>Coordinates:</b> {d['lat']}, {d['lon']}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- WEATHER ----------------
elif page == "☀️ Weather":
st.markdown('<div class="section">☀️ Travel Weather</div>', unsafe_allow_html=True)

destination = st.selectbox("Select destination", list(places.keys()))

st.info(
"This demo uses a simple travel-weather panel. "
"For live weather, connect a weather API such as OpenWeather."
)

weather = {
"Goa":("☀️","29°C","Sunny"),
"Kashmir":("⛅","18°C","Partly Cloudy"),
"Jaipur":("☀️","31°C","Sunny"),
"Kerala":("🌧️","27°C","Rainy"),
"Manali":("⛅","16°C","Cool"),
"Agra":("☀️","30°C","Sunny")
}

icon,temp,status = weather[destination]
c1,c2,c3 = st.columns(3)
c1.metric("Temperature", temp)
c2.metric("Condition", status)
c3.metric("Best for", "Sightseeing")

st.markdown(f"""
<div class="card">
<h1 style="font-size:70px">{icon}</h1>
<h2>{destination}</h2>
<p>Check the live forecast before finalizing your trip.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- TRIP PLANNER ----------------
elif page == "✈️ Trip Planner":
st.markdown('<div class="section">✈️ Build Your Trip</div>', unsafe_allow_html=True)

destination = st.selectbox("Destination", list(places.keys()))
start = st.date_input("Start date", date.today())
days = st.slider("Number of days", 1, 15, 4)
travelers = st.number_input("Travelers", 1, 10, 2)
budget = st.selectbox("Budget", ["Budget","Standard","Premium"])
interests = st.multiselect(
"Interests",
["🏖️ Beaches","🏔️ Mountains","🏛️ History","🍜 Food",
    "🛍️ Shopping","🌿 Nature","🎢 Adventure"]
)

end = start + timedelta(days=days-1)

st.markdown(f"""
<div class="card">
<h2>🧳 Your {days}-Day Plan</h2>
<p><b>📍 Destination:</b> {destination}</p>
<p><b>📅 Dates:</b> {start} → {end}</p>
<p><b>👥 Travelers:</b> {travelers}</p>
<p><b>💰 Budget:</b> {budget}</p>
<p><b>❤️ Interests:</b> {", ".join(interests) if interests else "Explore everything"}</p>
</div>
""", unsafe_allow_html=True)

if st.button("✨ Generate My Itinerary"):
st.success("Your personalized trip plan has been generated!")

for day in range(1, days + 1):
    st.write(
        f"**Day {day}:** Morning sightseeing → Local food 🍜 → "
        f"Afternoon exploration → Evening relaxation 🌅"
    )

# ---------------- WISHLIST ----------------
elif page == "❤️ Wishlist":
st.markdown('<div class="section">❤️ My Wishlist</div>', unsafe_allow_html=True)

if not st.session_state.wishlist:
st.info("Your wishlist is empty. Add destinations from Home.")
else:
for name in st.session_state.wishlist:
    st.markdown(
        f'<div class="card"><h3>❤️ {name}</h3>'
        f'<p>{places[name]["desc"]}</p></div>',
        unsafe_allow_html=True
    )

if st.button("🗑️ Clear Wishlist"):
    st.session_state.wishlist = []
    st.rerun()

# ---------------- REVIEWS ----------------
elif page == "⭐ Reviews":
st.markdown('<div class="section">⭐ Traveler Reviews</div>', unsafe_allow_html=True)

with st.form("review_form"):
name = st.text_input("Your name")
destination = st.selectbox("Destination", list(places.keys()))
rating = st.slider("Rating", 1, 5, 5)
review = st.text_area("Write your review")
submitted = st.form_submit_button("📤 Submit Review")

if submitted:
    if name and review:
        st.session_state.reviews.append({
            "name": name,
            "destination": destination,
            "rating": rating,
            "review": review
        })
        st.success("Review added!")
    else:
        st.warning("Please enter your name and review.")

for r in reversed(st.session_state.reviews):
st.markdown(f"""
<div class="card">
    <h3>👤 {r['name']} — {r['destination']}</h3>
    <p>{"⭐" * r['rating']}</p>
    <p>{r['review']}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- BOOKING ----------------
elif page == "🎫 Booking":
st.markdown('<div class="section">🎫 Book Your Adventure</div>', unsafe_allow_html=True)

with st.form("booking"):
name = st.text_input("Full Name")
email = st.text_input("Email")
destination = st.selectbox("Destination", list(places.keys()))
travel_date = st.date_input("Travel date", date.today())
travelers = st.number_input("Number of travelers", 1, 20, 1)
package = st.selectbox(
    "Package",
    ["Basic","Standard","Premium"]
)

submit = st.form_submit_button("🚀 Confirm Booking")

if submit:
    if name and email:
        st.session_state.bookings.append({
            "name":name,
            "email":email,
            "destination":destination,
            "date":travel_date,
            "travelers":travelers,
            "package":package
        })
        st.success(
            f"🎉 Booking request received for {destination}!"
        )
        st.balloons()
    else:
        st.warning("Please enter your name and email.")

# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align:center;padding:35px;color:#475569;">
<h3>🌍 Wanderly India</h3>
<p>Travel more • Explore more • Create memories ❤️</p>
<p>Built with Python 🐍 + Streamlit ⚡</p>
</div>
""", unsafe_allow_html=True)
