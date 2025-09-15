import streamlit as st
import random
from schedule_generator import generate_schedule

# ✅ Final Subjects (16 only)
subjects = {
    1: "Bahasa Melayu",
    2: "English",
    3: "Chinese",
    4: "Science",
    5: "Mathematics",
    6: "Sejarah",
    7: "Geografi",
    8: "Account",
    9: "Pendidikan Seni Visual",
    10: "Sains Komputer",
    11: "Pendidikan Moral",
    12: "Pendidikan Islam",
    13: "Additional Mathematics",
    14: "Physics",
    15: "Biologi",
    16: "Chemistry"
}

# ✅ Categories (3 only)
categories = ["Tingkatan 1-3", "Sastera", "Sains"]

# ✅ Streamlit Page Config
st.set_page_config(page_title="Penjana Jadual Ulang Kaji", layout="centered")

# 🎨 Motion Background (CSS + Animation)
st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stButton>button {
        border-radius: 12px;
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.title("📚 Penjana Jadual Ulang Kaji")

# ✅ Category Selection (One Only)
selected_category = st.selectbox("Pilih Kategori Murid:", categories)

# ✅ Subjects Selection with Select All / Clear All
st.subheader("Pilih Subjek:")
all_subjects = list(subjects.values())

# Session state for subjects
if "selected_subjects" not in st.session_state:
    st.session_state.selected_subjects = []

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Pilih Semua"):
        st.session_state.selected_subjects = all_subjects
with col2:
    if st.button("❌ Kosongkan Semua"):
        st.session_state.selected_subjects = []

selected_subjects = st.multiselect(
    "Pilih subjek:",
    options=all_subjects,
    default=st.session_state.selected_subjects,
    key="subjects_multiselect"
)

# ✅ Difficulty Selection (Auto appears after choosing subjects)
difficulties = {}
if selected_subjects:
    st.subheader("Pilih Tahap Kesukaran Setiap Subjek:")
    for subject in selected_subjects:
        difficulties[subject] = st.selectbox(
            f"Tahap kesukaran {subject}:",
            ["Mudah", "Sederhana", "Sukar"],
            key=f"difficulty_{subject}"
        )

# ✅ Generate Button
if st.button("🚀 Jana Jadual"):
    if not selected_subjects:
        st.error("⚠️ Sila pilih sekurang-kurangnya satu subjek.")
    else:
        schedule = generate_schedule(selected_subjects, difficulties)
        st.success("✅ Jadual berjaya dijana!")
        st.write(schedule)
