import streamlit as st
from groq import Groq
import os
import json

st.set_page_config(
    page_title="TriBe – Find Your Vibe",
    page_icon="🏨",
    layout="centered"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0F0F1A;
    color: #E5E7EB;
  }

  .stApp { background-color: #0F0F1A; }

  h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

  .tribe-hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
  }
  .tribe-logo {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    color: #A78BFA;
    letter-spacing: -1px;
    margin-bottom: 0.25rem;
  }
  .tribe-tagline {
    font-size: 1rem;
    color: #6B7280;
    font-style: italic;
    margin-bottom: 2rem;
  }

  .step-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #7C3AED;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
  }

  .vibe-chip {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.85rem;
    color: #A78BFA;
    margin: 0.2rem;
    cursor: pointer;
  }

  .hotel-card {
    background: #1A1A2E;
    border: 1px solid #2D2D44;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #7C3AED;
  }
  .hotel-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #F3F4F6;
    margin-bottom: 0.15rem;
  }
  .hotel-meta {
    font-size: 0.82rem;
    color: #6B7280;
    margin-bottom: 0.75rem;
  }
  .hotel-vibe-tag {
    display: inline-block;
    background: rgba(124,58,237,0.2);
    color: #A78BFA;
    border-radius: 12px;
    padding: 0.18rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-right: 0.4rem;
    margin-bottom: 0.5rem;
  }
  .hotel-why {
    font-size: 0.9rem;
    color: #D1D5DB;
    line-height: 1.6;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #2D2D44;
  }
  .nearby-section {
    margin-top: 0.6rem;
    font-size: 0.82rem;
    color: #9CA3AF;
  }
  .price-badge {
    float: right;
    background: rgba(16,185,129,0.15);
    color: #34D399;
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.85rem;
    font-weight: 500;
    font-family: 'Syne', sans-serif;
  }

  /* Streamlit widget overrides */
  .stSelectbox > div > div,
  .stSlider, .stTextInput > div > div {
    background-color: #1A1A2E !important;
    border-color: #2D2D44 !important;
    color: #E5E7EB !important;
  }
  .stButton > button {
    background: #7C3AED;
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.6rem 2rem;
    width: 100%;
    transition: background 0.2s;
  }
  .stButton > button:hover {
    background: #6D28D9;
    color: white;
  }
  .stSpinner > div { border-top-color: #7C3AED !important; }
  div[data-testid="stMarkdownContainer"] p { color: #D1D5DB; }
  .stAlert { background: #1A1A2E; border-color: #7C3AED; }
</style>
""", unsafe_allow_html=True)

# ─── MOCK HOTEL DATA ─────────────────────────────────────────────────────────
HOTELS = [
    {
        "id": 1,
        "name": "The Haveli House",
        "location": "Jaipur",
        "price_per_night": 2200,
        "rating": 4.6,
        "vibes": ["Heritage", "Cultural", "Aesthetic"],
        "amenities": ["Rooftop terrace", "Traditional Rajasthani meals", "Cultural evenings", "Heritage architecture", "Inner courtyard"],
        "nearby": ["Hawa Mahal (5 min)", "Local bazaars (2 min)", "Street food lane (1 min)"],
        "photos_note": "Guest photos show authentic stone walls, hand-painted murals, and marigold decorations",
        "description": "A restored 200-year-old haveli with original frescoes and architecture. Serves traditional dal baati churma and has nightly folk performances."
    },
    {
        "id": 2,
        "name": "The Workcation Nest",
        "location": "Goa",
        "price_per_night": 1800,
        "rating": 4.5,
        "vibes": ["Workation", "Social", "Chill"],
        "amenities": ["High-speed WiFi (200 Mbps)", "Co-working desks", "Social lounge", "Coffee bar", "Pool", "Community events"],
        "nearby": ["Baga Beach (10 min)", "Cafes (2 min)", "Supermarket (5 min)"],
        "photos_note": "Guest photos show open co-working spaces, hammocks by the pool, and community game nights",
        "description": "Purpose-built for remote workers. Ergonomic desks, fiber internet, and a community of like-minded digital nomads. Social events every Friday."
    },
    {
        "id": 3,
        "name": "Rishikesh River Camp",
        "location": "Rishikesh",
        "price_per_night": 1400,
        "rating": 4.4,
        "vibes": ["Adventure", "Nature", "Budget-friendly"],
        "amenities": ["Riverside location", "Bungee booking desk", "Bonfire nights", "Yoga sessions", "Rafting packages"],
        "nearby": ["Rafting starting point (2 min)", "Laxman Jhula (15 min)", "Cafes by the Ganga (5 min)"],
        "photos_note": "Guest photos show tents by the river, morning yoga with mountain views, and bonfire evenings",
        "description": "Glamping tents on the banks of the Ganges. Wake up to river sounds, book your rafting and bungee on-site, and end the day around a bonfire."
    },
    {
        "id": 4,
        "name": "The Calm Retreat",
        "location": "Coorg",
        "price_per_night": 3200,
        "rating": 4.8,
        "vibes": ["Wellness", "Peaceful", "Staycation"],
        "amenities": ["Spa", "Infinity pool", "Organic meals", "Forest walks", "Meditation sessions", "No TV policy"],
        "nearby": ["Coffee plantation (on-site)", "Waterfall trek (30 min)", "Local market (20 min)"],
        "photos_note": "Guest photos show misty mornings, jungle views from the infinity pool, and spa treatment rooms",
        "description": "A digital detox property nestled in a working coffee plantation. No TVs, no rush. Ayurvedic spa, guided forest walks, and farm-to-table meals."
    },
    {
        "id": 5,
        "name": "Zostel Manali",
        "location": "Manali",
        "price_per_night": 700,
        "rating": 4.3,
        "vibes": ["Adventure", "Budget-friendly", "Social"],
        "amenities": ["Common room", "Mountain views", "Travel desk", "Free breakfast", "Bonfire", "Group treks"],
        "nearby": ["Solang Valley (15 min)", "Mall Road (10 min)", "Snow point (20 min)"],
        "photos_note": "Guest photos show snowy mountain views, group bonfire moments, and cozy common room hangouts",
        "description": "The OG backpacker hostel in Manali. Vibrant community of solo travelers, organized group treks, and unbeatable views of the Himalayas at a price that won't break the bank."
    },
    {
        "id": 6,
        "name": "Bangala Heritage Bungalow",
        "location": "Chettinad",
        "price_per_night": 4500,
        "rating": 4.9,
        "vibes": ["Heritage", "Culinary", "Cultural"],
        "amenities": ["Cooking classes", "Antique furniture", "Heritage architecture", "Authentic Chettinad cuisine", "Guided heritage walks"],
        "nearby": ["Chettinad Palace (5 min)", "Spice markets (10 min)", "Temple complexes (2 min)"],
        "photos_note": "Guest photos show ornate Athangudi tile floors, teak pillars, and elaborate Chettinad thalis",
        "description": "A 100-year-old Nattukotai Chettiar mansion converted into a boutique hotel. World-famous for its Chettinad cooking classes and authentic local cuisine."
    },
    {
        "id": 7,
        "name": "The Loft Pondicherry",
        "location": "Pondicherry",
        "price_per_night": 2600,
        "rating": 4.7,
        "vibes": ["Aesthetic", "Peaceful", "Cultural"],
        "amenities": ["French Quarter location", "Courtyard garden", "Cafe attached", "Cycle rentals", "Art gallery"],
        "nearby": ["Promenade Beach (5 min)", "Auroville (20 min)", "French Quarter walks (immediate)"],
        "photos_note": "Guest photos show pastel yellow walls, bougainvillea courtyard, vintage French doors, and quiet reading nooks",
        "description": "A colonial-era villa in the heart of the French Quarter. Instagram-worthy at every corner — pastel walls, tiled floors, and a garden cafe that serves the best croissants in South India."
    },
    {
        "id": 8,
        "name": "Spiti Valley Homestay",
        "location": "Spiti",
        "price_per_night": 900,
        "rating": 4.5,
        "vibes": ["Adventure", "Offbeat", "Nature"],
        "amenities": ["Home-cooked meals", "Stargazing deck", "Local guide access", "Monastery visits", "Yak safari"],
        "nearby": ["Key Monastery (10 min)", "Chandratal Lake (2 hour trek)", "Local village (5 min)"],
        "photos_note": "Guest photos show stark barren landscapes, milky way nights, and warm homestay interiors",
        "description": "A local family-run homestay at 12,000 feet. The most authentic way to experience Spiti — home-cooked Spitian food, stories by the fire, and access to routes tourists rarely find."
    }
]

VIBE_OPTIONS = ["Heritage & Culture", "Workation", "Adventure", "Wellness & Peaceful", "Budget Backpacker", "Aesthetic & Instagrammable", "Offbeat & Hidden Gems", "Not sure yet"]

LOCATION_VIBE_MAP = {
    "jaipur": ["Heritage & Culture", "Aesthetic & Instagrammable"],
    "goa": ["Workation", "Adventure", "Budget Backpacker"],
    "rishikesh": ["Adventure", "Wellness & Peaceful"],
    "manali": ["Adventure", "Budget Backpacker"],
    "coorg": ["Wellness & Peaceful", "Offbeat & Hidden Gems"],
    "pondicherry": ["Aesthetic & Instagrammable", "Wellness & Peaceful"],
    "spiti": ["Offbeat & Hidden Gems", "Adventure"],
    "chettinad": ["Heritage & Culture"],
    "mumbai": ["Workation", "Aesthetic & Instagrammable"],
    "delhi": ["Heritage & Culture", "Workation"],
    "bangalore": ["Workation", "Budget Backpacker"],
}

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "welcome"
if "location" not in st.session_state:
    st.session_state.location = ""
if "budget" not in st.session_state:
    st.session_state.budget = 2000
if "vibe" not in st.session_state:
    st.session_state.vibe = ""
if "results" not in st.session_state:
    st.session_state.results = None


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def get_suggested_vibes(location: str) -> list[str]:
    loc = location.lower().strip()
    for key, vibes in LOCATION_VIBE_MAP.items():
        if key in loc:
            return vibes
    return ["Adventure", "Heritage & Culture", "Wellness & Peaceful"]


def filter_hotels(location: str, budget: int, vibe: str) -> list[dict]:
    """Rule-based filter: location match or any hotel if no match, then budget, then vibe."""
    loc = location.lower().strip()

    # Try location match first
    location_matched = [h for h in HOTELS if loc in h["location"].lower()]
    pool = location_matched if location_matched else HOTELS

    # Budget filter (within 50% above budget for flexibility)
    budget_filtered = [h for h in pool if h["price_per_night"] <= budget * 1.5]
    if not budget_filtered:
        budget_filtered = sorted(pool, key=lambda h: h["price_per_night"])[:5]

    # Vibe match — normalize
    vibe_keyword = vibe.split(" ")[0].lower() if vibe and vibe != "Not sure yet" else ""
    if vibe_keyword:
        vibe_matched = [h for h in budget_filtered if any(vibe_keyword in v.lower() for v in h["vibes"])]
        if vibe_matched:
            return vibe_matched[:5]

    return budget_filtered[:5]


def get_ai_explanation(hotel: dict, user_location: str, user_budget: int, user_vibe: str) -> str:
    """Call Groq to generate a personalised vibe explanation for a hotel."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are TriBe, an AI hotel discovery agent for GenZ solo travelers in India.

A user is looking for a hotel with these preferences:
- Location: {user_location}
- Budget: ₹{user_budget}/night
- Trip vibe: {user_vibe}

Here is a hotel to explain:
Name: {hotel['name']}
Location: {hotel['location']}
Price: ₹{hotel['price_per_night']}/night
Vibes: {', '.join(hotel['vibes'])}
Amenities: {', '.join(hotel['amenities'])}
Description: {hotel['description']}
Guest photo note: {hotel['photos_note']}

Write a SHORT, punchy 2-3 sentence explanation of WHY this hotel matches the user's vibe specifically.
Be direct and conversational — talk to a GenZ traveler.
Mention one specific detail that proves the vibe is real (not generic).
Do NOT start with "This hotel" — be creative with the opening.
Keep it under 60 words."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ─── UI ──────────────────────────────────────────────────────────────────────

st.markdown('<div class="tribe-hero"><div class="tribe-logo">TriBe</div><div class="tribe-tagline">Find your vibe. Book your stay.</div></div>', unsafe_allow_html=True)

# ── STEP 1: WELCOME ──
if st.session_state.step == "welcome":
    st.markdown("### Plan your next trip")
    st.markdown("Answer 3 quick questions and get a shortlist of hotels that actually match your vibe — with explanations.")
    st.markdown("")
    if st.button("Let's go →"):
        st.session_state.step = "questions"
        st.rerun()

# ── STEP 2: QUESTIONS ──
elif st.session_state.step == "questions":
    st.markdown("### Tell us about your trip")
    st.markdown("")

    st.markdown('<div class="step-label">1 — Where are you headed?</div>', unsafe_allow_html=True)
    location = st.text_input("", placeholder="e.g. Goa, Jaipur, Manali, Rishikesh...", key="loc_input", label_visibility="collapsed")

    st.markdown("")
    st.markdown('<div class="step-label">2 — What\'s your budget per night?</div>', unsafe_allow_html=True)
    budget = st.slider("", min_value=500, max_value=10000, value=2000, step=500,
                       format="₹%d", label_visibility="collapsed")
    st.markdown(f"<p style='color:#A78BFA; font-size:0.9rem; margin-top:-0.5rem;'>Up to ₹{budget:,}/night</p>", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="step-label">3 — What\'s your trip vibe?</div>', unsafe_allow_html=True)

    # If location entered, show suggested vibes
    suggested = []
    if location and location.strip():
        suggested = get_suggested_vibes(location)
        st.markdown(f"<p style='font-size:0.8rem; color:#6B7280;'>Based on {location.strip().title()}, you might like:</p>", unsafe_allow_html=True)
        chips_html = "".join([f'<span class="vibe-chip">✨ {v}</span>' for v in suggested])
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("")

    vibe = st.selectbox("", VIBE_OPTIONS, index=7, label_visibility="collapsed")

    st.markdown("")
    if st.button("Find my hotels →"):
        if not location.strip():
            st.error("Please enter a location!")
        else:
            st.session_state.location = location.strip()
            st.session_state.budget = budget
            st.session_state.vibe = vibe if vibe != "Not sure yet" else (suggested[0] if suggested else "Adventure")
            st.session_state.step = "results"
            st.rerun()

# ── STEP 3: RESULTS ──
elif st.session_state.step == "results":
    loc = st.session_state.location
    budget = st.session_state.budget
    vibe = st.session_state.vibe

    st.markdown(f"### 🏨 Your {vibe} shortlist in {loc.title()}")
    st.markdown(f"<p style='color:#6B7280; font-size:0.85rem;'>Budget: up to ₹{budget:,}/night</p>", unsafe_allow_html=True)
    st.markdown("")

    # Filter hotels
    matched = filter_hotels(loc, budget, vibe)

    if not matched:
        st.warning("No hotels found for this combination. Try adjusting your budget or vibe.")
    else:
        for hotel in matched:
            with st.spinner(f"Analysing {hotel['name']}..."):
                try:
                    explanation = get_ai_explanation(hotel, loc, budget, vibe)
                except Exception:
                    explanation = hotel["description"]

            vibe_tags = "".join([f'<span class="hotel-vibe-tag">{v}</span>' for v in hotel["vibes"]])
            nearby_list = " · ".join([f"📍 {n}" for n in hotel["nearby"][:2]])

            st.markdown(f"""
<div class="hotel-card">
  <div>
    <span class="price-badge">₹{hotel['price_per_night']:,}/night</span>
    <div class="hotel-name">{hotel['name']}</div>
    <div class="hotel-meta">📍 {hotel['location']} &nbsp;·&nbsp; ⭐ {hotel['rating']}</div>
    {vibe_tags}
    <div class="hotel-why">🤖 <em>{explanation}</em></div>
    <div class="nearby-section">{nearby_list}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Start over"):
            for key in ["step", "location", "budget", "vibe", "results"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with col2:
        if st.button("🔁 Change vibe"):
            st.session_state.step = "questions"
            st.rerun()
