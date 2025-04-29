import streamlit as st
import requests

# 🔧 This MUST be the first Streamlit command
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

st.title("🤖 AI Lead Qualifier Bot (Demo)")
st.write("Enter a potential lead's **email** and **company name**, and this tool will tell you if it's worth qualifying!")

email = st.text_input("Your email?")
company = st.text_input("Company name?")

if st.button("Submit"):

    if not email or not company:
        st.error("Please enter both email and company name.")
    else:
        with st.spinner("Thinking..."):

            api_key = st.secrets["OPENROUTER_API_KEY"]  # ✅ Make sure your key is in Streamlit secrets

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            system_prompt = "You are a startup analyst AI that evaluates whether a lead is worth qualifying."
            user_prompt = f"Here is the email: {email}\nCompany name: {company}\nShould we qualify this lead?"

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "mistralai/mixtral-8x7b",  # ✅ Valid model name
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                )
                data = response.json()

                if "choices" in data:
                    st.success("✅ Response from AI:")
                    st.markdown(data["choices"][0]["message"]["content"])
                else:
                    st.error(f"Something went wrong: {data.get('error', {}).get('message', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error: {e}")
