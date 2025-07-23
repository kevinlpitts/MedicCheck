import streamlit as st
import requests
import time

API_URL = "https://mediccheck-backend.onrender.com"

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

st.set_page_config(page_title="MedicCheck 🌍💊", page_icon="💊", layout="centered")
st.title("🌍 MedicCheck – Medication Equivalents")

st.markdown("Easily find international equivalents for medications across countries 🌐.")

# Debounced API call with caching
@st.cache_data(ttl=60)
def fetch_equivalents(name):
    payload = {"med_name": name, "country": None}
    try:
        res = requests.post(f"{API_URL}/medications", json=payload, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as err:
        return {"error": str(err)}

med_name = st.text_input("🔎 Search by medication or brand name", placeholder="e.g. Paracetamol")

if med_name.strip():
    with st.spinner("Searching for equivalents..."):
        time.sleep(0.3)  # UX: simulate debounce delay
        data = fetch_equivalents(med_name)

        if "error" in data:
            st.error(f"⚠️ API error: {data['error']}")
        elif data["equivalents"]:
            st.success(f"🌍 International equivalents for **{data['original']}**:")
            for country, brand in data["equivalents"].items():
                flag = flag_emojis.get(country, "")
                st.markdown(f"- {flag} **{country}**: {brand}")
        else:
            st.info("ℹ️ No equivalents found. Try another name.")
else:
    st.info("ℹ️ Enter a medication name above to get started.")
