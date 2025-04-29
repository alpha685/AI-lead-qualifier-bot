import streamlit as st
import requests
import json

# ✅ MUST be at the very top before anything else
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")
 
# ✅ Load secret safely
api_key = st.secrets["openrouter"].get("api_key", None)

if not api_key:
    st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    st.stop()

st.title("🤖 AI Lead Qualifier Bot")
st.write("Enter a LinkedIn lead description, and I’ll qualify them based on your Ideal Customer Profile.")

# ✅ Step 1: Load the API key securely
api_key = st.secrets.get("OPENROUTER_API_KEY")

# ✅ DEBUGGING INFO
st.write("🔍 DEBUG – Is key loaded?", bool(api_key))
st.write("🔍 DEBUG – Key value:", api_key[:10] + "..." if api_key else "Not Found")

# ✅ Step 2: Streamlit input form
lead_description = st.text_area("Paste the LinkedIn lead description here")
submit = st.button("Qualify Lead")

# ✅ Step 3: API call function
def qualify_lead(description):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mixtral-8x7b",
        "messages": [
            {"role": "system", "content": "You are an AI lead qualification agent. Evaluate if a lead is a fit based on a given ICP."},
            {"role": "user", "content": description}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            return message
        except Exception as e:
            return f"❌ Something went wrong parsing the response: {e}"
    else:
        return f"❌ OpenRouter API error: {response.json()}"

# ✅ Step 4: Trigger on submission
if submit:
    if not api_key:
        st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    elif not lead_description.strip():
        st.warning("⚠️ Please enter a lead description.")
    else:
        with st.spinner("🔍 Qualifying lead..."):
            result = qualify_lead(lead_description)
            st.success("✅ Lead Qualification Result:")
            st.write(result)
