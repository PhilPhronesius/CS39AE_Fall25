import streamlit as st
from pathlib import Path

st.title("👋 My Bio")

# ---------- TODO: Replace with your own info ----------
NAME = "Phil Phronesius"
PROGRAM = "Computer Science"
INTRO = (
    "Hi, everybody. My name is Phil Phronesius and I am currently a CS student. What I really enjoy about data visualization are the different types of graphs I got to make. My most favorite would be the Lab 3.1 where we made a world map to visualize a trip."
)
FUN_FACTS = [
    "I love food.",
    "I’m learning Data Visualization.",
    "I want to build something fun.",
]
def find_photo(filename="your_photo.jpg"):
    # Photo was saved in assets folder
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path.cwd()
 
    candidates = [
        script_dir / "assets" / "your_photo.jpg",          # pages/assets/...
        script_dir.parent / "assets" / "your_photo.jpg",   # root/assets/... (common)
        Path("assets") / "your_photo.jpg",                 # cwd/assets/...
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None
 
photo_src = find_photo("your_photo.jpg")  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center") 

with col1: 
    if photo_src:
        st.image(photo_src, caption=NAME, width=250)
    else:
        st.info( "📷 Place Ren_Photo.jpg inside an assets/ folder at the app root " 
                "or update the path in find_photo()." )
        
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")
    
st.divider()
st.caption("Edit pages/1_Bio.py to customize this page.")
