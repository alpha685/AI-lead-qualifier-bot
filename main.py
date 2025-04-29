import streamlit as st
import requests
import json

import json

# Your NoCodeAPI endpoint
NOCODE_API_URL = "https://v1.nocodeapi.com/advik/google_sheets/czdwCjQIvd"

def save_lead(name, email, company):
    data = [[name, email, company]]
    response = requests.post(NOCODE_API_URL, json={"data": data})
    if response.status_code == 200:
        print("Lead saved successfully!")
    else:
        print(f"Failed to save lead: {response.text}")
        
name = st.text_input("What’s your name?")
email = st.text_input("Your email?")
company = st.text_input("Company name?")
submitted = st.button("Submit")

if submitted:
    save_lead(name, email, company)
    st.success(f"Thanks {name}! Let's qualify your lead 👇")

# After user submits the form:
if submitted:
    save_lead(name, email, company)
    st.success(f"Thanks {name}! Let's qualify your lead 👇")



st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

st.title("🤖 AI Lead Qualifier Bot (Demo)")
st.markdown("You're a smart AI assistant that asks 3 questions to qualify a lead for a digital marketing agency.")

with st.form("lead_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    company = st.text_input("Your Company Name")
    submitted = st.form_submit_button("Start Qualifying Lead")

if submitted:
    st.success(f"Thanks {name}! Let's qualify your lead 👇")

    # --- THEN your chat input starts ---
    user_input = st.text_input("Your answer here...")

# Your API settings
API_URL = "https://openrouter.ai/api/v1/chat/completions"  # Change if needed
API_KEY ="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"
MODEL = "openai/gpt-3.5-turbo"  # ✅ Pick a working model here!

# User input
user_input = st.chat_input("Your answer here...")

if user_input:
    with st.spinner("Thinking..."):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You're a smart AI assistant that asks 3 questions to qualify a lead for a digital marketing agency."},
                {"role": "user", "content": user_input},
            ],
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raises HTTPError for bad HTTP status codes

            response_json = response.json()

            # Check for API-level error inside JSON
            if 'error' in response_json:
                st.error(f"API Error: {response_json['error']['message']}")
                st.stop()

            # Otherwise, proceed
            reply = response_json['choices'][0]['message']['content']
            st.chat_message("assistant").markdown(reply)

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
        except KeyError:
            st.error("Unexpected API response format. Please check your API provider and model.")
