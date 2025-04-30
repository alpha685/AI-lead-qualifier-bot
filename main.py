import streamlit as st
import requests

# Set Streamlit page configuration (must be FIRST)
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

st.title("AI Lead Qualifier Bot")
st.write("Enter a LinkedIn lead description, and I’ll qualify them based on your Ideal Customer Profile.")

# Load the OpenRouter API key securely from Streamlit secrets
api_key = st.secrets.get("OPENROUTER_API_KEY", None)

# Debugging output
st.markdown(f"🔍 **DEBUG – Is key loaded?** {api_key is not None}")
st.markdown(f"🔍 **DEBUG – Key value:** {'sk-or-' + api_key[-8:] if api_key else 'Not Found'}")

# Input box for user to enter LinkedIn lead description
lead_description = st.text_area("Paste the LinkedIn lead description here", height=150)

if st.button("Qualify Lead"):
    if not api_key:
        st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    elif not lead_description.strip():
        st.error("❌ Please enter a valid lead description.")
    else:
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openrouter/cinematika-7b",
                        "messages": [
                            {"role": "system", "content": "You are an AI sales analyst. Given a lead description, decide if they match a B2B SaaS company’s ideal customer profile (ICP). Respond with ✅ Qualified or ❌ Not Qualified, and give one-line reasoning."},
                            {"role": "user", "content": lead_description}
                        ]
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    reply = result["choices"][0]["message"]["content"]
                    st.success("✅ Lead Qualification Result:")
                    st.write(reply)
                else:
                    st.error(f"❌ API request failed: {response.status_code} – {response.text}")

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
