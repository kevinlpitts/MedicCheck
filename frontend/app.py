import streamlit as st
import requests

API_URL = "http://mediccheck-backend.onrender.com"
"

st.set_page_config(page_title="MedicCheck 🌍💊", page_icon="💊")
st.title("🌍 MedicCheck – Medication Equivalents")

with st.form("search_form"):
    med_name = st.text_input("Active ingredient or brand name", placeholder="e.g. Paracetamol")
    submitted = st.form_submit_button("Find equivalents →")

if submitted:
    if not med_name.strip():
        st.warning("Please enter a medication name.")
    else:
        payload = {"med_name": med_name, "country": None}
        try:
            res = requests.post(f"{API_URL}/medications", json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
            if data["equivalents"]:
                st.success(f"International equivalents for **{data['original']}**:")
                for country, brand in data["equivalents"].items():
                    st.markdown(f"- **{country}**: {brand}")
            else:
                st.info("No equivalents found (yet). Try another name.")
        except requests.RequestException as err:
            st.error(f"API error: {err}")
