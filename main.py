import streamlit as st
import requests

# Set page configuration (MUST be the first Streamlit call)
st.set_page_config(page_title="🤖 AI Lead Qualifier Bot (Demo)")

st.title("🤖 AI Lead Qualifier Bot")
st.markdown("This AI agent qualifies leads based on company name and email.")

# Input fields
email = st.text_input("Enter the lead's email:")
company = st.text_input("Enter the lead's company name:")
submit = st.button("Qualify Lead")

# Load OpenRouter API key
api_key = st.secrets.get("OPENROUTER_API_KEY")
if not api_key:
    st.error("❌ API key not found. Please set `OPENROUTER_API_KEY` in Streamlit secrets.")
    st.stop()

if submit:
    if not email or not company:
        st.warning("Please enter both an email and a company name.")
    else:
        prompt = f"""You are a B2B SaaS startup advisor. Given this lead info:

Email: {email}
Company: {company}

1. Is this a qualified lead? (Yes/No)
2. Why or why not?
3. Give a confidence score (0-100).
Only reply in this format:

Qualified: Yes/No  
Reason: [Your explanation]  
Confidence: [Number between 0-100]
"""

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "mistralai/mixtral-8x7b",
                    "messages": [
                        {"role": "system", "content": "You are a helpful SaaS startup advisor."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            data = response.json()
            if response.status_code == 200 and "choices" in data:
                result = data["choices"][0]["message"]["content"]
                st.success("✅ Lead Analysis")
                st.markdown(result)
            else:
                st.error(f"❌ OpenRouter API error: {data}")
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
