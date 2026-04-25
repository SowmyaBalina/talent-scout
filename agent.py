import streamlit as st
import json
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# --- Initialize Groq LLM ---
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(page_title="TalentScout Chat", page_icon="💬")
st.title("🕵️‍♂️ TalentScout AI Copilot")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask me to find candidates (e.g., 'Find me a Python Dev')"):
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Agent Execution ---
    with st.chat_message("assistant"):
        with st.spinner("Analyzing talent pool..."):
            try:
                # Load candidates
                talent_file = os.path.join(os.path.dirname(__file__), 'talent.json')
                with open(talent_file, 'r') as f:
                    candidates_pool = json.load(f)

                # Define the Agent
                scout = Agent(
                    role='Recruitment Assistant',
                    goal='Answer the user\'s recruiting questions based on the candidate pool.',
                    backstory='You are a helpful hiring assistant. You provide clear tables and summaries.',
                    llm=groq_llm,
                    verbose=True
                )

                # Define the Task based on the USER PROMPT
                chat_task = Task(
                    description=f"User Request: {prompt}. Data: {json.dumps(candidates_pool)}. Provide a detailed answer. If ranking candidates, use ONLY Markdown table format with pipes (|) - NO HTML tags whatsoever.",
                    expected_output="A helpful response using only Markdown format (especially for tables). Do not use any HTML tags like <font>, <b>, <br>, etc.",
                    agent=scout
                )

                crew = Crew(agents=[scout], tasks=[chat_task])
                result = crew.kickoff()
                
                # Display and Save response
                response_text = result.raw
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Error: {e}")