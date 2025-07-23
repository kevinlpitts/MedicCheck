import streamlit as st
import requests

API_URL = "https://mediccheck-backend.onrender.com"

st.set_page_config(page_title="MedicCheck 🌍💊", page_icon="💊")
st.title("🌍 MedicCheck – Medication Equivalents")

st.markdown(
    "🌐 *Find internationally recognized brand names for the medications you know and trust.*\n"
    "✈️ Perfect for travel, relocation, or global healthcare planning."
)

with st.form("search_form"):
    med_name = st.text_input("🔍 Active ingredient or brand name", placeholder="e.g. Paracetamol, Tylenol, Nurofen")
    submitted = st.form_submit_button("Find Equivalents →")

if submitted:
    if not med_name.strip():
        st.warning("Please enter a medication name.")
    else:
        payload = {"med_name": med_name, "country": None}
        with st.spinner("🔎 Looking up international equivalents..."):
            try:
                res = requests.post(f"{API_URL}/medications", json=payload, timeout=10)
                res.raise_for_status()
                data = res.json()

                if data["equivalents"]:
                    st.success(f"🌍 International equivalents for **{data['original']}**:")
                    for country, brand in data["equivalents"].items():
                        # Attempt to generate country flag emoji from country name
                        flag = ""
                        country_code_map = {
                            "USA": "us", "UK": "gb", "India": "in", "France": "fr", "Germany": "de",
                            "Canada": "ca", "Australia": "au", "Spain": "es", "Italy": "it", "Japan": "jp"
                        }
                        code = country_code_map.get(country, "").lower()
                        if code:
                            flag = f":flag-{code}:"

                        cols = st.columns([1, 5])
                        cols[0].markdown(f"{flag}")
                        cols[1].markdown(f"**{country}** → {brand}")
                else:
                    st.info("No equivalents found (yet). Try another name.")

            except requests.RequestException as err:
                st.error(f"⚠️ API error: {err}")
