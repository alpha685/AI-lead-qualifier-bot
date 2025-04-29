import streamlit as st
import requests
import os

# ✅ This must be the first Streamlit command
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

st.title("🤖 AI Lead Qualifier Bot (Demo)")
st.write("Enter a potential lead's **email** and **company name**, and this tool will tell you if it's worth qualifying!")

# Get user input
email = st.text_input("Your email?")
company = st.text_input("Company name?")
submit = st.button("Submit")

if submit:
    with st.spinner("🤖 Thinking..."):

        # ✅ Load your OpenRouter API key securely from secrets
        api_key = st.secrets["OPENROUTER_API_KEY"]

        # ✅ Headers for OpenRouter
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-lead-qualifier-bot.streamlit.app/",
            "X-Title": "AI Lead Qualifier Bot"
        }

        # ✅ The message we're sending to the model
        messages = [
            {
                "role": "user",
                "content": f"Is the company '{company}' (lead email: {email}) a good fit for an AI B2B product? Respond with reasoning and a decision: 'Qualify' or 'Disqualify'."
            }
        ]

        # ✅ Request payload for OpenRouter
        payload = {
            "model": "mistralai/mixtral-8x7b",
            "messages": messages
        }

        try:
            # Send request
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            result = response.json()

            # ✅ Check for 'choices' key safely
            if "choices" in result and len(result["choices"]) > 0:
                output = result["choices"][0]["message"]["content"]
                st.success("✅ Here's the analysis:")
                st.write(output)
            else:
                st.error(f"❌ OpenRouter API error: {result.get('error', 'Unknown issue. Check your API key and model.')}")
                st.json(result)  # Show the whole JSON for debugging

        except Exception as e:
            st.error(f"Something went wrong: {e}")
