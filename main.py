import streamlit as st
import requests

# Set page config (must be first Streamlit call)
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

# Load API key
api_key = st.secrets.get("OPENROUTER_API_KEY", "")

# Debugging: Display key presence (safe version)
st.markdown("### AI Lead Qualifier Bot")
st.write("Enter a LinkedIn lead description, and I’ll qualify them based on your Ideal Customer Profile.\n")

st.markdown(f"🔍 **DEBUG – Is key loaded?** {'True' if api_key else 'False'}")
st.markdown(f"🔍 **DEBUG – Key value:** {'sk-...'+api_key[-6:] if api_key else 'Not Found'}")

# Input form
user_input = st.text_area("Paste the LinkedIn lead description here")

if st.button("Qualify Lead"):
    if not api_key:
        st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    elif not user_input:
        st.warning("Please enter a LinkedIn lead description.")
    else:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://your-app-name.streamlit.app",  # optional but recommended
                    "X-Title": "AI Lead Qualifier"
                },
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a B2B SaaS lead qualification assistant. Based on a LinkedIn profile summary, determine if the lead is qualified according to typical Ideal Customer Profiles (ICPs) like VP of Marketing, Head of Sales at Series A-C startups in the US/Europe."
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                lead_reply = result['choices'][0]['message']['content']
                st.success("✅ Lead Qualification Result:")
                st.markdown(lead_reply)
            else:
                st.error(f"❌ API request failed: {response.status_code} – {response.text}")
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
