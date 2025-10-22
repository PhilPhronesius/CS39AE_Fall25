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
        script_dir / "assets" / filename,          # pages/assets/...
        script_dir.parent / "assets" / filename,   # root/assets/... (common)
        Path("assets") / filename,                 # cwd/assets/...
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None
 
photo_src = find_photo("your_photo.jpg")  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    try:
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    except Exception:
        st.info("Add a photo named `your_photo.jpg` to the repo root, or change PHOTO_PATH.")
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
