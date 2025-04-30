import streamlit as st
import requests

# ✅ Must be first
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

st.title("AI Lead Qualifier Bot")
st.write("Enter a LinkedIn lead description, and I’ll qualify them based on your Ideal Customer Profile.")

# DEBUG: Show if the key is found
api_key = st.secrets.get("OPENROUTER_API_KEY", None)
st.write(f"\n🔍 DEBUG – Is key loaded? {api_key is not None}")
st.write(f"🔍 DEBUG – Key value: {api_key[:10] + '...' if api_key else 'Not Found'}")

# Input from user
lead_description = st.text_area("Paste the LinkedIn lead description here")

if st.button("Qualify Lead"):
    if not api_key:
        st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    elif not lead_description:
        st.warning("Please enter a lead description.")
    else:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://your-username.streamlit.app",  # Optional but helpful
                    "X-Title": "AI Lead Qualifier"
                },
                json={
                    "model": "mistralai/mixtral-8x7b",
                    "messages": [
                        {"role": "system", "content": "You are an AI lead qualification assistant."},
                        {"role": "user", "content": lead_description}
                    ]
                }
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Lead Qualification Result:")
                st.write(result["choices"][0]["message"]["content"])
            else:
                st.error(f"❌ API request failed: {response.status_code} – {response.text}")

        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
