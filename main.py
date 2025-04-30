import streamlit as st
import requests
import os

# Set page config first
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)", layout="centered")

st.title("AI Lead Qualifier Bot")
st.write("Enter a LinkedIn lead description, and I’ll qualify them based on your Ideal Customer Profile.")

# Load OpenRouter API key from secrets
api_key = st.secrets.get("OPENROUTER_API_KEY", None)

# Debugging
st.write("🔍 DEBUG – Is key loaded?", api_key is not None)
st.write("🔍 DEBUG – Key value:", api_key[:10] + "..." if api_key else "Not Found")

# Text input
user_input = st.text_area("Paste the LinkedIn lead description here", height=200)

if st.button("🔎 Qualify Lead"):
    if not api_key:
        st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    elif not user_input.strip():
        st.warning("⚠️ Please enter a lead description.")
    else:
        # Custom ICP Prompt
        prompt = f"""
You are an AI assistant helping qualify B2B leads based on an Ideal Customer Profile (ICP).

ICP criteria:
- Role: Decision makers (VPs, Heads, Directors)
- Department: Marketing or Growth
- Company Stage: Series A–C
- Team size: 10–50
- Geography: North America or Europe
- AI Usage: Actively exploring or implementing AI

Given the following lead description, analyze how well this lead matches the ICP.

Respond with:
- Match Score (0–100)
- Reasons for the score
- Red or green flags
- Suggested action

Lead description:
\"\"\"
{user_input}
\"\"\"
"""

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=60
            )

            if response.status_code == 200:
                response_text = response.json()["choices"][0]["message"]["content"]
                st.success("✅ Lead Qualification Result:")
                st.write(response_text)

                # Download button
                st.download_button(
                    label="📥 Download Result",
                    data=response_text,
                    file_name="lead_qualification_result.txt",
                    mime="text/plain"
                )

            else:
                st.error(f"❌ API request failed: {response.status_code} – {response.text}")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

