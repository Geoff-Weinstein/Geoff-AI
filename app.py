import streamlit as st
import openai
import json

# Set your OpenAI API key here
openai.api_key = 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
st.set_page_config(page_title="Geoff AI", layout="centered")

st.title("🧠 Geoff AI — Strategic Communication Analyzer")
st.markdown("Simulate Geoff Weinstein’s expert feedback on your written communication.")

# --- Input Section ---
audience = st.selectbox("Who is your audience?", [
    "Senior Executive",
    "Team Leader",
    "Peer/Colleague",
    "Client/Customer",
    "Cross-functional Stakeholder",
    "General Public"
])

outcome = st.text_input("What do you want your audience to think, feel, know, or do?")

message = st.text_area("Paste your message here (email, proposal, etc.)", height=250)

if st.button("Analyze My Message"):
    with st.spinner("Analyzing like Geoff would..."):
        prompt = f"""
You are an AI communication coach modeled after Geoff Weinstein.
Analyze the following message for clarity, influence, tone, and strategic alignment.

The user wants their audience to {outcome}.
The audience is: {audience}.

Message:
\"\"\"{message}\"\"\"

For each of the following dimensions, assign a score from 1 to 5 and provide a short commentary:
1. Readability
2. Structure
3. Visual Design
4. Influencing Capacity
5. Psychological Techniques
6. Tone & Emotional Resonance
7. Cognitive Overload & Friction
8. Call-to-Action Clarity
9. Credibility Signals

Use Geoff’s voice: encouraging, direct, strategic, and reflective.
Use the phrase “Cut the fluff!” if the message is too wordy.
Return the results in structured JSON format.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            result = response['choices'][0]['message']['content']

            try:
                feedback = json.loads(result)
                st.subheader("📊 Feedback Summary")

                for dimension, data in feedback.items():
                    st.markdown(f"**{dimension}** — Score: {data['score']}/5")
                    st.write(data['commentary'])
                    if "Cut the fluff!" in data['commentary']:
                        st.warning("✂️ Cut the fluff!")

            except json.JSONDecodeError:
                st.error("⚠️ Could not parse GPT response. Try simplifying your message or reloading.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
