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

st.title("📡 Simple Live Data Demo (Open-Meteo)")
st.caption("Friendly demo with manual refresh + fallback data so it never crashes.")

lat, lon = 39.7392, -104.9903  # Denver

wurl = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
@st.cache_data(ttl=600, show_spinner=False)

def get_weather():
    try:
        r = requests.get(wurl, timeout=10); r.raise_for_status()
        j = r.json()["current"]
        return pd.DataFrame([{"time": pd.to_datetime(j["time"]),
                          "temperature": j["temperature_2m"],
                          "wind": j["wind_speed_10m"]}])

    except requests.RequestException as e:
        return pd.DataFrame([{
            "time": "Error",
            "temperature": f"Error: {e}",
            "wind": "Error"}])

  # --- Auto Refresh Controls ---
st.subheader("🔁 Auto Refresh Settings")

# Let user choose how often to refresh (in seconds)
refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)

# Toggle to turn automatic refreshing on/off
auto_refresh = st.toggle("Enable auto-refresh", value=False)

# Show current refresh time
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

if "temperature_history" not in st.session_state:
    st.session_state.temperature_history = []
    
st.dataframe(df, use_container_width=True)

df = get_weather()

if isinstance(df, pd.DataFrame) and not df.empty and "temperature" in df.columns:
    st.session_state.temperature_history.append({
        "time": df["time"].iloc[0],
        "temperature": df["temperature"].iloc[0]})

temperature_df = pd.DataFrame(st.session_state.temperature_history)

fig = px.line(df, x="time", y=["temperature"],
              labels = {"time": "Time", "temperature": "Temp. (°C)"},
              title=f"Current Weather")
fig.update_traces(mode="markers+lines")

st.plotly_chart(fig, use_container_width=True)

# If auto-refresh is ON, wait and rerun the app
if auto_refresh:
    time.sleep(refresh_sec)
    get_weather.clear()
    st.rerun()
