import streamlit as st
import requests

# ✅ Set Streamlit page config FIRST
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

# ✅ Load API key from Streamlit secrets
api_key = st.secrets.get("openrouter", {}).get("api_key", None)

# ✅ Debug info
st.title("AI Lead Qualifier Bot")
st.markdown("Enter a LinkedIn lead description, and I’ll qualify them based on your Ideal Customer Profile.")
st.write("🔍 DEBUG – Is key loaded?", api_key is not None)
st.write("🔍 DEBUG – Key value:", api_key if api_key else "Not Found")

# ✅ If no API key, show error and stop
if not api_key:
    st.error("❌ API key not found. Make sure it’s set in Streamlit secrets.")
    st.stop()

# ✅ Text input for user
lead_description = st.text_area("Paste the LinkedIn lead description here")

# ✅ When user clicks the button
if st.button("Qualify Lead"):
    if not lead_description.strip():
        st.warning("⚠️ Please enter a valid lead description.")
        st.stop()

    # ✅ Make the API call to OpenRouter
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mixtral-8x7b",
                "messages": [
                    {"role": "system", "content": "You are a startup sales analyst. Assess the lead based on ICP fit."},
                    {"role": "user", "content": lead_description}
                ]
            }
        )
        response.raise_for_status()
        data = response.json()

        # ✅ Extract result
        result = data["choices"][0]["message"]["content"]
        st.success("✅ Lead Qualification Result:")
        st.write(result)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
    except KeyError:
        st.error(f"❌ OpenRouter API error: {response.json()}")
