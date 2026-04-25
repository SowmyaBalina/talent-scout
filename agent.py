import streamlit as st
import json
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# =================================================================
# 1. LOAD ENVIRONMENT & CONFIGURATION
# =================================================================

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Safety Check
if not groq_api_key:
    st.error("❌ GROQ_API_KEY Not Found! Please check your .env file.")
    st.stop()

# Initialize Groq LLM via CrewAI's LLM class
# Llama 3.3 70B is perfect for complex reasoning tasks like recruitment
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key
)

# =================================================================
# 2. UI FRONTEND (Streamlit)
# =================================================================

st.set_page_config(page_title="AI Talent Scout (Groq Edition)", layout="wide", page_icon="⚡")

st.title("⚡ Ultra-Fast AI Talent Scouting Agent")
st.markdown("""
    This agent uses **Groq LPU™ technology** and **Llama 3.3** to analyze candidates in seconds.
""")

st.sidebar.title("System Status")
st.sidebar.success("Connected to Groq Cloud")
st.sidebar.info("Model: Llama-3.3-70b")

jd_input = st.text_area(
    "Paste the Job Description (JD):",
    height=150,
    placeholder="e.g. Seeking a Python Developer with 5+ years experience..."
)

# =================================================================
# 3. CORE AGENT LOGIC
# =================================================================

if st.button("🚀 Start High-Speed Scouting"):
    if not jd_input:
        st.error("Please provide a Job Description.")
    else:
        try:
            # Load your candidate database
            talent_file = os.path.join(os.path.dirname(__file__), 'talent.json')
            with open(talent_file, 'r') as f:
                candidates_pool = json.load(f)
            
            st.info(f"Loaded {len(candidates_pool)} profiles. Starting Multi-Agent Analysis...")

            # Agent 1: The Technical Matcher
            researcher = Agent(
                role='Technical Talent Matcher',
                goal='Compare candidate skills against the JD and assign a Match Score (0-100).',
                backstory="""You are an expert technical recruiter. You focus on hard skills, 
                years of experience, and tech stack compatibility. You are precise and objective.""",
                llm=groq_llm,
                verbose=True,
                allow_delegation=False
            )

            # Agent 2: The Engagement Expert
            engager = Agent(
                role='Candidate Engagement Specialist',
                goal='Analyze candidate sentiment and assign an Interest Score (0-100).',
                backstory="""You analyze the 'last_outreach_response' to see if the candidate 
                is excited, neutral, or uninterested in new opportunities.""",
                llm=groq_llm,
                verbose=True
            )

            # Task 1: Technical Ranking
            match_task = Task(
                description=f"""
                JD: {jd_input}
                Candidates: {json.dumps(candidates_pool)}
                Action: Evaluate every candidate. Provide a Match Score and a brief reasoning.
                """,
                expected_output="A list of technical match evaluations.",
                agent=researcher
            )

            # Task 2: Final Report Generation
            scoring_task = Task(
                description="""
                Review the previous evaluations. 
                Now, analyze the 'last_outreach_response' for each candidate to give an Interest Score.
                Combine everything into a final Markdown Table with: 
                Name, Match Score, Interest Score, and a 'Final Verdict'.
                """,
                expected_output="A clean Markdown table ranking the candidates.",
                agent=engager
            )

            # Execute the Crew
            with st.spinner("Agents are thinking at the speed of Groq..."):
                recruit_crew = Crew(
                    agents=[researcher, engager],
                    tasks=[match_task, scoring_task],
                    process=Process.sequential
                )
                final_report = recruit_crew.kickoff()

            # Display results
            st.success("Scouting Complete!")
            st.markdown("### 📋 Final Ranked Candidate Shortlist")
            st.markdown(final_report.raw)

        except FileNotFoundError:
            st.error("Error: 'talent.json' not found in the current directory.")
        except Exception as e:
            st.error(f"Execution Error: {e}")

# =================================================================
# 4. HOW TO RUN
# =================================================================
# 1. pip install crewai langchain_groq streamlit python-dotenv
# 2. Add GROQ_API_KEY to your .env
# 3. streamlit run agent.py