import streamlit as st
import json
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# =================================================================
# 1. LOAD ENVIRONMENT & CONFIGURATION
# =================================================================

# This reads the .env file and makes the variables available to the script
load_dotenv()

# Get the key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Safety Check: If the key is missing, stop the app and alert the user
if not api_key:
    st.error("❌ API Key Not Found! Please ensure you have a '.env' file with GEMINI_API_KEY=your_key")
    st.stop()

# Initialize the Gemini LLM (Free Tier: Gemini 2.0 Flash)
gemini_llm = LLM(
    # model="gemini/gemini-2.0-flash",
    model="gemini-3-pro-preview",
    api_key=api_key,
    max_rpm=10
)

# =================================================================
# 2. UI FRONTEND (Streamlit)
# =================================================================

st.set_page_config(page_title="AI Talent Scout", layout="wide", page_icon="🕵️‍♂️")

# Sidebar for metadata and project info
st.sidebar.title("Agent Controls")
st.sidebar.markdown("""
**Requirements Met:**
- ✅ JD Parsing
- ✅ Candidate Discovery
- ✅ Explainable Matching
- ✅ Interest Scoring
""")
st.sidebar.divider()
st.sidebar.info("System uses a local JSON database as requested.")

st.title("🕵️‍♂️ AI-Powered Talent Scouting & Engagement Agent")
st.markdown("### Step 1: Input Job Requirements")

# User inputs the Job Description
jd_input = st.text_area(
    "Paste the Job Description (JD) below:",
    height=200,
    placeholder="e.g. We need a Senior Python Developer with 5+ years of experience in Django..."
)

st.markdown("---")

# =================================================================
# 3. CORE AGENT LOGIC
# =================================================================

if st.button("🚀 Start Scouting & Assessment"):
    if not jd_input:
        st.error("Please provide a Job Description to begin.")
    else:
        try:
            # Load the local JSON database (talents.json)
            with open('talents.json', 'r') as f:
                candidates_pool = json.load(f)
            
            st.info(f"Successfully connected to talent.json. Analyzing {len(candidates_pool)} profiles...")

            # Agent 1: The Researcher / Matcher
            researcher = Agent(
                role='Talent Matching Specialist',
                goal='Analyze candidate technical fit against the provided JD.',
                backstory="""You are a veteran technical recruiter. You look for skill overlap, 
                years of experience, and technical depth. You provide clear reasoning for your scores.""",
                llm=gemini_llm,
                max_iter=3,
                verbose=True,
                allow_delegation=False
            )

            # Agent 2: The Engagement Analyst
            engager = Agent(
                role='Candidate Engagement Scorer',
                goal='Evaluate the interest and availability of candidates based on their last communication.',
                backstory="""You are an expert in candidate relations. You analyze the sentiment of 
                their last outreach response to see if they are actually open to new roles.""",
                llm=gemini_llm,
                verbose=True
            )

            # Task 1: Technical Matching
            match_task = Task(
                description=f"""
                1. Compare this JD: {jd_input}
                2. Against these Candidates: {json.dumps(candidates_pool)}
                3. Assign a 'Match Score' (0-100) based on skills and seniority.
                4. Provide a 'Match Justification' for each person.
                """,
                expected_output="A list of candidates with Match Scores and reasoning.",
                agent=researcher
            )

            # Task 2: Sentiment & Ranking
            scoring_task = Task(
                description="""
                1. Review the candidates identified in the previous step.
                2. Analyze their 'last_outreach_response' from the data.
                3. Assign an 'Interest Score' (0-100) based on their availability/sentiment.
                4. Output a Final Shortlist in a Markdown Table with Match Score, Interest Score, and Recommendation.
                """,
                expected_output="A Markdown table ranking candidates by a combined score.",
                agent=engager
            )

            # Execute the Crew
            with st.spinner("Multi-Agent orchestration in progress..."):
                recruit_crew = Crew(
                    agents=[researcher, engager],
                    tasks=[match_task, scoring_task],
                    process=Process.sequential
                )
                final_report = recruit_crew.kickoff()

            # Display results
            st.success("Analysis Complete!")
            st.markdown("### 📋 Final Ranked Candidate Shortlist")
            st.markdown(final_report.raw)

        except FileNotFoundError:
            st.error("Error: 'talent.json' not found. Please ensure it is in the same folder as agent.py.")
        except Exception as e:
            st.error(f"Execution Error: {e}")

# =================================================================
# 4. HOW TO RUN
# =================================================================
# 1. pip install crewai streamlit python-dotenv
# 2. Create a .env file with GEMINI_API_KEY=xxxx
# 3. Run: streamlit run agent.py