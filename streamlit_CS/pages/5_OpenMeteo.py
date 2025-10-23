import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Live API Demo (Simple)", page_icon="📡", layout="wide")
# Disable fade/transition so charts don't blink between reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)

st.title("📡 Simple Live Data Demo (CoinGecko)")
st.caption("Friendly demo with manual refresh + fallback data so it never crashes.")

COINS = ["bitcoin", "ethereum"]
VS = "usd"
HEADERS = {"User-Agent": "msudenver-dataviz-class/1.0", "Accept": "application/json"}

def build_url(ids):
    return f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies={VS}"

API_URL = build_url(COINS)

# Tiny sample to keep the demo working even if the API is rate-limiting
SAMPLE_DF = pd.DataFrame(
    [{"coin": "bitcoin", VS: 68000}, {"coin": "ethereum", VS: 3500}]
)

lat, lon = 39.7392, -104.9903  # Denver

wurl = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
@st.cache_data(ttl=600, show_spinner=False)

def get_weather():
    r = requests.get(wurl, timeout=10); r.raise_for_status()
    j = r.json()["current"]
    return pd.DataFrame([{"time": pd.to_datetime(j["time"]),
                          "temperature": j["temperature_2m"],
                          "wind": j["wind_speed_10m"]}])

  # --- Auto Refresh Controls ---
st.subheader("🔁 Auto Refresh Settings")

# Let user choose how often to refresh (in seconds)
refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)

# Toggle to turn automatic refreshing on/off
auto_refresh = st.toggle("Enable auto-refresh", value=False)

# Show current refresh time
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

st.subheader("Prices")
df, err = get_weather(API_URL)

if err:
    st.warning(f"{err}\nShowing sample data so the demo continues.")
    df = SAMPLE_DF.copy()

st.dataframe(df, use_container_width=True)

fig = px.bar(df, x="coin", y=VS, title=f"Current price ({VS.upper()})")
st.plotly_chart(fig, use_container_width=True)

# If auto-refresh is ON, wait and rerun the app
if auto_refresh:
    time.sleep(refresh_sec)
    get_weather.clear()
    st.rerun()
