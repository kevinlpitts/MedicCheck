import streamlit as st
import requests

API_URL = "https://mediccheck-backend.onrender.com"

# Emoji flags for countries
flag_emojis = {
    "USA": "🇺🇸",
    "UK": "🇬🇧",
    "India": "🇮🇳",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Japan": "🇯🇵",
    "Canada": "🇨🇦",
    "Australia": "🇦🇺"
}

# Page configuration
st.set_page_config(page_title="MedicCheck 🌍💊", page_icon="💊", layout="centered")
st.markdown(
    "<h1 style='text-align: center;'>🌍 MedicCheck – Medication Equivalents</h1>",
    unsafe_allow_html=True
)

# Search form section
with st.form("search_form"):
    st.markdown("### 🔍 Search for a medication")
    med_name = st.text_input("Active ingredient or brand name", placeholder="e.g. Paracetamol")
    submitted = st.form_submit_button("Find equivalents →")

# Results section
if submitted:
    if not med_name.strip():
        st.warning("⚠️ Please enter a medication name.")
    else:
        payload = {"med_name": med_name, "country": None}
        try:
            res = requests.post(f"{API_URL}/medications", json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
            if data["equivalents"]:
                st.markdown(f"## 🌐 Equivalents for **{data['original']}**:")
                for country, brand in data["equivalents"].items():
                    flag = flag_emojis.get(country, "🏳️")
                    st.markdown(f"""
                    <div style='border:1px solid #eee; padding:10px; border-radius:10px; margin-bottom:8px; background-color:#f9f9f9'>
                        <span style='font-size:24px;'>{flag}</span> <strong>{country}</strong>: {brand}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ No equivalents found. Try a different name.")
        except requests.RequestException as err:
            st.error(f"❌ API error: {err}")
