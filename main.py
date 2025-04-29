import streamlit as st

# MUST be first Streamlit command
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

import requests
import json

st.title("🤖 AI Lead Qualifier Bot (Demo)")
st.markdown("Enter a potential lead's **email** and **company name**, and this tool will tell you if it's worth qualifying!")

email = st.text_input("Your email?")
company = st.text_input("Company name?")
submit = st.button("Submit")

if submit:
    if not email or not company:
        st.warning("Please fill in both fields.")
    else:
        with st.spinner("Analyzing lead..."):
            headers = {
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json",
            }

            system_prompt = (
                "You are an AI trained to qualify B2B leads. "
                "Given an email and company name, analyze whether the lead is promising. "
                "Return a short reasoning and a verdict: 'Qualified' or 'Not Qualified'."
            )

            user_prompt = f"Email: {email}\nCompany: {company}\nShould we qualify this lead?"

            payload = {
                "model": "openrouter/mistralai/mixtral-8x7b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }

            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                result = response.json()
                output = result['choices'][0]['message']['content']
                st.success("✅ Result:")
                st.write(output)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
