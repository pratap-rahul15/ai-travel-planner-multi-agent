import os
import re
from datetime import datetime

import folium
from streamlit_folium import st_folium

import streamlit as st
from langchain_core.messages import HumanMessage
from main import app
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background:
        radial-gradient(circle at top, rgba(34, 92, 164, 0.18), transparent 26%),
        linear-gradient(180deg, #070b12 0%, #090f18 45%, #070b12 100%);
    color: #e7f1fb;
}

#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d16 0%, #0a101b 100%) !important;
    border-right: 1px solid #162235 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown {
    color: #a9c7e1 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #17243a !important;
}

.sidebar-title {
    color: #e7f1fb;
    font-size: 1.02rem;
    font-weight: 700;
    margin: 1rem 0 0.5rem;
    letter-spacing: 0.02em;
}

.sidebar-chip {
    background: rgba(17, 26, 43, 0.92);
    border: 1px solid #1a2d46;
    border-radius: 10px;
    padding: 0.52rem 0.8rem;
    margin-bottom: 0.42rem;
    font-size: 0.85rem;
    color: #8fb8db;
}

input[type="text"], .stTextInput input {
    background: #0d1624 !important;
    border: 1px solid #1a2b42 !important;
    border-radius: 10px !important;
    color: #e7f1fb !important;
}

input[type="text"]:focus, .stTextInput input:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.18) !important;
}

input[type="text"]::placeholder { color: #52708d !important; }

.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label {
    color: #7eb9f0 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
}

.stTextArea textarea {
    background: #0a1522 !important;
    border: 1px solid #1f3048 !important;
    border-radius: 14px !important;
    color: #eff7ff !important;
    font-size: 0.97rem !important;
    resize: none !important;
    padding: 0.9rem !important;
}

.stTextArea textarea:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.18) !important;
}

.stTextArea textarea::placeholder { color: #577594 !important; }

.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #cfe2f4 !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #eff7ff !important;
}

.stMarkdown code {
    background: #0e1a2b !important;
    color: #8ec3ff !important;
    padding: 0.15em 0.45em;
    border-radius: 5px;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d70c9 0%, #0f579d 55%, #0b437c 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.9rem 1.2rem !important;
    font-size: 1.03rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    box-shadow: 0 0 28px rgba(29,112,201,0.35), 0 8px 20px rgba(0,0,0,0.35) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 42px rgba(29,112,201,0.6), 0 10px 26px rgba(0,0,0,0.45) !important;
}

div[data-testid="stDownloadButton"] > button {
    background: #173457 !important;
    color: #e8f4ff !important;
    border: 1px solid #294d7d !important;
    border-radius: 12px !important;
    width: 100% !important;
}

.stAlert {
    background: #0e1726 !important;
    border-radius: 12px !important;
}

.stAlert p, .stAlert div { color: #e0edf8 !important; }

.hero-wrapper {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin: 0.4rem 0 1.4rem;
    min-height: 320px;
    border: 1px solid rgba(126, 180, 231, 0.12);
    box-shadow: 0 18px 50px rgba(0,0,0,0.35);
}

.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.38) saturate(1.02);
    position: absolute;
    top: 0;
    left: 0;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(135deg, rgba(7, 11, 18, 0.82), rgba(7, 11, 18, 0.3)),
        linear-gradient(to bottom, rgba(0,0,0,0.12), rgba(0,0,0,0.58));
}

.hero-content {
    position: relative;
    z-index: 2;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}

.hero-badge {
    background: rgba(58,123,213,0.2);
    border: 1px solid rgba(58,123,213,0.42);
    color: #8cc7ff !important;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    padding: 0.35rem 0.95rem;
    border-radius: 999px;
    margin-bottom: 0.9rem;
    display: inline-block;
    backdrop-filter: blur(12px);
}

.hero-title {
    font-size: clamp(2rem, 4vw, 3.45rem);
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.55rem;
    line-height: 1.1;
}

.hero-sub {
    color: #a8c2db;
    font-size: 1rem;
    max-width: 760px;
    line-height: 1.7;
}

.hero-stats {
    display: flex;
    gap: 0.9rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 1.35rem;
}

.hero-stat {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.60);
    backdrop-filter: blur(14px);
    border-radius: 14px;
    min-width: 140px;
    padding: 0.85rem 1rem;
}

.hero-stat h3 {
    margin: 0;
    color: #ffffff;
    font-size: 1.12rem;
    font-weight: 800;
}

.hero-stat p {
    margin: 0.18rem 0 0;
    color: #93b7d9;
    font-size: 0.78rem;
}

.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.8rem 0 0.8rem;
    padding-bottom: 0.55rem;
    border-bottom: 1px solid #1b2a40;
}

.sec-head span {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e7f1fb;
}

.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.2rem 0 1.4rem;
}

.metric-box {
    flex: 1;
    background: rgba(14, 22, 35, 0.92);
    border: 1px solid #1c2c43;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    text-align: center;
}

.metric-val {
    font-size: 1.75rem;
    font-weight: 800;
    color: #54a8ff;
}

.metric-lbl {
    font-size: 0.78rem;
    color: #86aed0 !important;
    margin-top: 0.15rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.final-card {
    background: linear-gradient(160deg, #0c1726 0%, #09111c 100%);
    border: 1px solid #1f3857;
    border-left: 4px solid #3a7bd5;
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    line-height: 1.85;
    color: #d5e8f8;
    font-size: 0.96rem;
}

.save-bar {
    background: #0e1623;
    border: 1px solid #1d2d45;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    color: #8cb8db !important;
    font-size: 0.9rem;
    margin-top: 0.55rem;
}

.save-bar code {
    color: #8ec3ff !important;
    background: #09111c !important;
}

.glass-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
    backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    box-shadow: 0 14px 30px rgba(0,0,0,0.18);
}

.workflow-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.9rem;
    margin: 0.2rem 0 1rem;
}

.workflow-card {
    background: rgba(14, 22, 35, 0.92);
    border: 1px solid #1b2a40;
    border-radius: 16px;
    padding: 1rem 0.9rem;
    text-align: center;
}

.workflow-icon {
    font-size: 1.6rem;
    margin-bottom: 0.4rem;
}

.workflow-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e7f1fb;
    margin: 0;
}

.workflow-sub {
    font-size: 0.76rem;
    color: #8daecf;
    margin: 0.25rem 0 0;
}

.nav-wrap {
    margin: 0.1rem 0 1rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.75rem;
    border-bottom: 1px solid #1b2a40;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(14, 22, 35, 0.9);
    border-radius: 12px 12px 0 0;
    padding: 0.7rem 1rem;
    color: #9fc2e6;
}

.stTabs [aria-selected="true"] {
    background: #173457 !important;
    color: #ffffff !important;
}

.timeline-wrapper {
    position: relative;
    margin-top: 1rem;
}

.timeline-line {
    position: absolute;
    left: 18px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, #2f6db5, rgba(47,109,181,0.1));
}

.timeline-card {
    position: relative;
    margin-left: 3rem;
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.timeline-dot {
    position: absolute;
    left: -2.55rem;
    top: 1.2rem;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #3a7bd5;
    border: 3px solid #08111d;
    box-shadow: 0 0 18px rgba(58,123,213,0.7);
}

.timeline-day {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.9rem;
}

.timeline-item {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 0.75rem;
    color: #d4e6f7;
    line-height: 1.7;
}

.timeline-icon {
    min-width: 28px;
    font-size: 1rem;
}

.timeline-label {
    font-weight: 700;
    color: #8fc4ff;
}


section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d16 0%, #0a101b 100%) !important;
    border-right: 1px solid #162235 !important;
}


button[kind="header"] {
    background: rgba(17, 26, 43, 0.92) !important;
    border: 1px solid #1a2d46 !important;
    border-radius: 10px !important;
    color: #8fc4ff !important;
    width: 42px !important;
    height: 42px !important;
    top: 12px !important;
    left: 12px !important;
    transition: all 0.2s ease !important;
    z-index: 9999 !important;
}

button[kind="header"]:hover {
    background: #173457 !important;
    color: white !important;
    box-shadow: 0 0 18px rgba(58,123,213,0.5);
}



section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #dbeafe !important;
}



/* Hotel cards */

.hotel-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.hotel-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1rem;
    backdrop-filter: blur(16px);
    transition: all 0.25s ease;
    box-shadow: 0 10px 22px rgba(0,0,0,0.18);
}

.hotel-card:hover {
    transform: translateY(-4px);
    border-color: rgba(58,123,213,0.45);
    box-shadow: 0 16px 28px rgba(0,0,0,0.28);
}

.hotel-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.7rem;
}

.hotel-badge {
    display: inline-block;
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    background: rgba(58,123,213,0.18);
    color: #8fc4ff;
    font-size: 0.72rem;
    margin-right: 0.4rem;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(58,123,213,0.28);
}

.hotel-desc {
    color: #cfe2f4;
    line-height: 1.7;
    font-size: 0.9rem;
}

</style>
""",
    unsafe_allow_html=True,
)


with st.sidebar:

    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    page = option_menu(
        menu_title=None,
        options=[
            "Plan Trip",
            "Saved Trips",
            "Analytics",
            "About"
        ],
        icons=[
            "airplane",
            "bookmark-heart",
            "bar-chart",
            "info-circle"
        ],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "0",
                "background-color": "transparent"
            },
            "icon": {
                "color": "#8fbdf2",
                "font-size": "16px"
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#122038",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background-color": "#173457",
                "color": "#ffffff",
            },
        },
    )

    st.markdown(
        "<div class='sidebar-title'>🌍 AI Travel Copilot</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = "Rahul Pratap Singh"

    thread_id = st.text_input(
        "👤 User ID",
        value=st.session_state["thread_id"],
        help="Your session ID — keeps travel history across queries",
    )

    st.session_state["thread_id"] = thread_id

    st.markdown(
        "<div class='sidebar-title'>Powered by</div>",
        unsafe_allow_html=True
    )

    for tech in [
        "🔗 LangGraph",
        "🧠 Groq · Llama 3.3 70B",
        "🐘 PostgreSQL",
        "🔍 Tavily Search",
        "✈️ AviationStack",
    ]:
        st.markdown(
            f"<div class='sidebar-chip'>{tech}</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='sidebar-title'>Agent Pipeline</div>",
        unsafe_allow_html=True
    )

    for step in [
        "① Flight Agent",
        "② Hotel Agent",
        "③ Itinerary Agent",
        "④ Final Agent"
    ]:
        st.markdown(
            f"<div class='sidebar-chip'>{step}</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='sidebar-title'>Workspace</div>",
        unsafe_allow_html=True
    )


    

def load_saved_trips():

    save_dir = os.path.join(
        os.path.dirname(__file__),
        "travel_plans"
    )

    if not os.path.exists(save_dir):
        return []

    files = sorted(
        os.listdir(save_dir),
        reverse=True
    )

    return [
        file for file in files
        if file.endswith(".md")
    ]



if page == "Saved Trips":

    st.markdown(
        "<div class='sec-head'><span>📁 Saved Travel Plans</span></div>",
        unsafe_allow_html=True,
    )

    saved_files = load_saved_trips()

    if not saved_files:

        st.info("No saved trips yet.")

    else:

        for file in saved_files:

            file_path = os.path.join(
                os.path.dirname(__file__),
                "travel_plans",
                file
            )

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            with st.expander(f"📄 {file}"):

                st.markdown(content)

                st.download_button(
                    label="⬇️ Download",
                    data=content,
                    file_name=file,
                    mime="text/markdown",
                    use_container_width=True,
                    key=file
                )

    st.stop()




st.markdown(
    """
<div class="hero-wrapper">
    <img class="hero-bg"
         src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1800&q=90"
         alt="airplane above clouds"/>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-badge">✦ Powered by LangGraph + Llama 3.3 70B</div>
        <div class="hero-title">AI Travel Copilot</div>
        <div class="hero-sub">
            Multi-agent travel system that intelligently plans flights, hotels, and itineraries with real-time search, memory, and a polished SaaS-style experience.
        </div>
        <div class="hero-stats">
            <div class="hero-stat"><h3>4</h3><p>AI Agents</p></div>
            <div class="hero-stat"><h3>Live</h3><p>Real-time APIs</p></div>
            <div class="hero-stat"><h3>Stateful</h3><p>PostgreSQL Memory</p></div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

def render_destination_map():

    destination_map = folium.Map(
        location=[20, 0],
        zoom_start=3,
        tiles="CartoDB dark_matter"
    )

    locations = [
    ("India", 20.5937, 78.9629),
    ("Tokyo", 35.6762, 139.6503),
    ("Paris", 48.8566, 2.3522),
    ("Dubai", 25.2048, 55.2708),
    ("Rome", 41.9028, 12.4964),
    ("Bangkok", 13.7563, 100.5018),
]

    for city, lat, lon in locations:

        folium.Marker(
            [lat, lon],
            popup=f"🌍 {city}",
            tooltip=city,
            icon=folium.Icon(
                color="blue",
                icon="plane",
                prefix="fa"
            ),
        ).add_to(destination_map)

    st.markdown(
        '''
        <div class='sec-head'>
            <span>🗺️ Popular Travel Destinations</span>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st_folium(
        destination_map,
        width=None,
        height=420,
    )


def render_hotel_cards(hotel_text):

    if not hotel_text:
        st.markdown(
            "<div class='glass-card'>No hotels found.</div>",
            unsafe_allow_html=True
        )
        return

    hotel_lines = [
        line.strip()
        for line in hotel_text.split("\n")
        if line.strip()
    ]

    st.markdown(
        "<div class='hotel-grid'>",
        unsafe_allow_html=True
    )

    for line in hotel_lines[:6]:

        card = f"""
        <div class='hotel-card'>

            <div class='hotel-title'>
                🏨 Premium Stay
            </div>

            <div>
                <span class='hotel-badge'>⭐ AI Recommended</span>
                <span class='hotel-badge'>💰 Best Value</span>
            </div>

            <div class='hotel-desc'>
                {line}
            </div>

        </div>
        """

        st.markdown(
            card,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


DESTINATIONS = [
    ("🇯🇵 Tokyo", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome", "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(
            f"""
            <div style="border-radius:14px;overflow:hidden;position:relative;height:96px;">
                <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.58);" />
                <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;
                            color:#fff;font-size:0.8rem;font-weight:700;letter-spacing:0.01em;">
                    {name}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

render_destination_map()

st.markdown("<div class='sec-head'><span>🗺️ Describe your trip</span></div>", unsafe_allow_html=True)

QUICK = [
    "7-day Japan under ₹2L",
    "Paris trip for 5 days",
    "Dubai weekend trip",
    "Bali backpacking 10 days",
]

if "draft_query" not in st.session_state:
    st.session_state["draft_query"] = ""

qcols = st.columns(4)
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"quick_{label}"):
            st.session_state["draft_query"] = label

user_query = st.text_area(
    "",
    value=st.session_state.get("draft_query", ""),
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
    height=110,
    label_visibility="collapsed",
)

generate = st.button("🚀 Generate My Travel Plan", use_container_width=True)

AGENT_META = {
    "flight_agent": ("✈️", "Flight Agent", "Searching routes and timing"),
    "hotel_agent": ("🏨", "Hotel Agent", "Finding stays and value"),
    "itinerary_agent": ("🗓️", "Itinerary Agent", "Building day-wise plan"),
    "final_agent": ("🧠", "Final Agent", "Composing final response"),
}


def _empty_collection():
    return {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0,
    }


if "latest_plan" not in st.session_state:
    st.session_state["latest_plan"] = _empty_collection()
if "latest_query" not in st.session_state:
    st.session_state["latest_query"] = ""


def render_itinerary_timeline(itinerary_text):
    if not itinerary_text:
        st.markdown(
            "<div class='glass-card'>No itinerary generated.</div>",
            unsafe_allow_html=True,
        )
        return

    days = re.split(r"(Day\s+\d+[:\-]?.*)", itinerary_text)

    if len(days) < 2:
        st.markdown(
            f"<div class='glass-card'>{itinerary_text}</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        "<div class='timeline-wrapper'><div class='timeline-line'></div>",
        unsafe_allow_html=True,
    )

    i = 1
    while i < len(days):
        day_title = days[i].strip()
        content = days[i + 1].strip() if i + 1 < len(days) else ""

        lines = [line.strip() for line in content.split("\n") if line.strip()]

        st.markdown(
            f"""
            <div class="timeline-card">
                <div class="timeline-dot"></div>
                <div class="timeline-day">{day_title}</div>
            """,
            unsafe_allow_html=True,
        )

        for line in lines:
            icon = "📍"
            label = ""
            lower = line.lower()

            if "morning" in lower:
                icon = "☀️"
                label = "Morning"
            elif "afternoon" in lower:
                icon = "🌆"
                label = "Afternoon"
            elif "evening" in lower:
                icon = "🌙"
                label = "Evening"
            elif "night" in lower:
                icon = "🌃"
                label = "Night"

            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-icon">{icon}</div>
                    <div>
                        <span class="timeline-label">{label}</span><br>
                        {line}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
        i += 2

    st.markdown("</div>", unsafe_allow_html=True)


if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        st.session_state["latest_query"] = user_query
        config = {"configurable": {"thread_id": thread_id}}
        collected = _empty_collection()

        st.markdown(
            "<div class='sec-head'><span>🤖 Live Agent Pipeline</span></div>",
            unsafe_allow_html=True,
        )

        workflow_cols = st.columns(4)
        for col, (_, label, sub) in zip(workflow_cols, AGENT_META.values()):
            with col:
                st.markdown(
                    f"""
                    <div class="workflow-card">
                        <div class="workflow-icon">⏳</div>
                        <p class="workflow-title">{label}</p>
                        <p class="workflow-sub">{sub}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label, _ = AGENT_META.get(node_name, ("🔧", node_name, ""))
                with st.status(f"{icon} {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        collected["flight_results"] = state_update.get("flight_results", "")
                        st.markdown(collected["flight_results"] or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        collected["hotel_results"] = state_update.get("hotel_results", "")
                        st.markdown(collected["hotel_results"] or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        collected["itinerary"] = state_update.get("itinerary", "")
                        st.markdown(collected["itinerary"] or "_No itinerary generated._")

                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        collected["final_response"] = msgs[-1].content if msgs else ""
                        st.markdown(collected["final_response"] or "_No final response._")

                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        st.session_state["latest_plan"] = collected

        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric-box">
                    <div class="metric-val">4</div>
                    <div class="metric-lbl">Agents Run</div>
                </div>
                <div class="metric-box">
                    <div class="metric-val">{collected['llm_calls']}</div>
                    <div class="metric-lbl">LLM Calls</div>
                </div>
                <div class="metric-box">
                    <div class="metric-val">✅</div>
                    <div class="metric-lbl">Pipeline Status</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tabs = st.tabs(["✈ Flights", "🏨 Hotels", "🗓 Itinerary", "🧠 Final Plan"])

        
        with tabs[0]:
            st.markdown(
            "<div class='glass-card'>",
            unsafe_allow_html=True
        )

            st.markdown(
            collected["flight_results"] or "No flights found."
        )

            st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        with tabs[1]:

            st.markdown(
            "<div class='sec-head'><span>🏨 Recommended Hotels</span></div>",
            unsafe_allow_html=True,
        )

            st.markdown(
            "<div class='hotel-grid'>",
            unsafe_allow_html=True
        )

            render_hotel_cards(
            collected["hotel_results"]
        )

            st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        with tabs[2]:

            st.markdown(
            "<div class='sec-head'><span>🗓️ AI Generated Travel Timeline</span></div>",
            unsafe_allow_html=True,
        )

            render_itinerary_timeline(
            collected["itinerary"]
        )


        with tabs[3]:

            st.markdown(
            "<div class='final-card'>",
            unsafe_allow_html=True
        )

            st.markdown(
            collected["final_response"] or "No final response."
        )

            st.markdown(
            "</div>",
            unsafe_allow_html=True
        )



        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls: {collected['llm_calls']}*
"""

        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button(
                "⬇️ Download Plan",
                data=file_content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )
        with info_col:
            st.markdown(
                f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                unsafe_allow_html=True,
            )

else:
    latest = st.session_state.get("latest_plan", _empty_collection())

    st.markdown("<div class='sec-head'><span>✨ Your workspace</span></div>", unsafe_allow_html=True)

    top_cols = st.columns([1.2, 1, 1, 1])
    with top_cols[0]:
        st.markdown(
            """
            <div class="glass-card">
                <h3 style="margin:0 0 0.35rem;color:#eff7ff;">SaaS-style multi-agent travel planning</h3>
                <p style="margin:0;color:#9eb8d5;line-height:1.7;">
                    Generate real-time travel suggestions using a flight agent, hotel agent, itinerary agent, and final response agent.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_cols[1]:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;">
                <div class="metric-val">4</div>
                <div class="metric-lbl">Agents</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_cols[2]:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;">
                <div class="metric-val">Live</div>
                <div class="metric-lbl">API Search</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_cols[3]:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;">
                <div class="metric-val">Stateful</div>
                <div class="metric-lbl">Memory</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tabs = st.tabs(["✈ Flights", "🏨 Hotels", "🗓 Itinerary", "🧠 Final Plan"])

    with tabs[0]:
        st.markdown("<div class='glass-card'>No flight data yet. Run the planner to generate it.</div>", unsafe_allow_html=True)
    with tabs[1]:
        st.markdown("<div class='glass-card'>No hotel data yet. Run the planner to generate it.</div>", unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("<div class='glass-card'>No itinerary yet. Run the planner to generate it.</div>", unsafe_allow_html=True)
    with tabs[3]:
        st.markdown("<div class='final-card'>Your final travel plan will appear here after generation.</div>", unsafe_allow_html=True)
