import streamlit as st
import json
import os
import re
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

# ============================================================
# 1. IMPROVED MATCHER - HANDLES NATURAL LANGUAGE QUERIES
# ============================================================
def get_strict_matches(query, file_path='talent.json'):
    """
    SMART MATCHING:
    1. Extracts minimum experience requirement (e.g., '5' from '5 years')
    2. Extracts core role keywords from natural language
    3. Matches candidates where:
       - Role contains all core keywords (handles variations like Engineer/Developer)
       - Experience is >= requirement (not less than)
    
    Examples:
    - "find me full stack developer with 5 years" → role="full stack developer", exp=5
    - "Senior Backend Engineer 8 years" → role="backend engineer", exp=8
    - "Data Scientist" → role="data scientist", exp=0 (no minimum)
    """
    if not os.path.exists(file_path):
        return []
        
    with open(file_path, 'r') as f:
        pool = json.load(f)
    
    query_lower = query.lower()
    
    # ─── STEP 1: Extract Minimum Experience ───
    # Matches patterns like "5", "5+", "5-10", "5 years", etc.
    numbers = re.findall(r'\d+', query_lower)
    required_exp = int(numbers[0]) if numbers else 0
    
    # ─── STEP 2: Extract Core Role Keywords ───
    # Remove filler words but keep role-related words
    clean_role = query_lower
    
    # Remove common filler phrases (order matters - longer phrases first)
    fillers = [
        "find me a", "find me", 
        "search for", "give me", "i want", "looking for",
        "with ", "and ", "also ", 
        "of experience", "years of experience",
        "years", "year", "exp", "yrs", 
        "experience", "required", "requirement",
        "+", "-", "of", "a", "the"
    ]
    
    for filler in fillers:
        clean_role = clean_role.replace(filler, " ")
    
    # Remove numbers (experience values) from role
    clean_role = re.sub(r'\d+', '', clean_role)
    
    # Remove extra spaces and punctuation, split into keywords
    clean_role = re.sub(r'\s+', ' ', clean_role).strip(",. ")
    role_keywords = clean_role.split()
    
    matches = []
    
    # ─── STEP 3: Match Against Candidates ───
    for candidate in pool:
        cand_role = candidate.get('role', '').lower()
        
        # Extract candidate's numeric experience
        cand_exp_raw = str(candidate.get('experience', '0'))
        cand_exp_match = re.search(r'\d+', cand_exp_raw)
        cand_exp_num = int(cand_exp_match.group()) if cand_exp_match else 0
        
        # Check experience gate: candidate must have >= required years
        if cand_exp_num < required_exp:
            continue
        
        # Check role match: ALL keywords from query must be in candidate role
        # This handles variations like "engineer" vs "developer"
        if role_keywords and all(keyword in cand_role for keyword in role_keywords):
            matches.append({
                "name": candidate['name'],
                "role": candidate['role'],
                "experience": candidate['experience']
            })
        elif not role_keywords and required_exp == 0:
            # Edge case: if query has no keywords and no exp requirement, 
            # don't filter by role
            matches.append({
                "name": candidate['name'],
                "role": candidate['role'],
                "experience": candidate['experience']
            })
            
    return matches


# ============================================================
# 2. GLOBAL UI & STATE
# ============================================================
st.set_page_config(page_title="AI Talent Scout", layout="wide")

st.markdown("<h1 style='text-align: center;'>AI-Powered Talent Scouting & Engagement Agent</h1>", unsafe_allow_html=True)
st.markdown("---")

if "step" not in st.session_state: st.session_state.step = "search"
if "shortlist" not in st.session_state: st.session_state.shortlist = []
if "chat_history" not in st.session_state: st.session_state.chat_history = {}
if "current_jd" not in st.session_state: st.session_state.current_jd = ""

groq_llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# ============================================================
# PHASE 1: SEARCH
# ============================================================
if st.session_state.step == "search":
    st.subheader("🕵️‍♂️ Phase 1: Precise Sourcing")
    jd_input = st.text_area("Recruiter Input / JD:", height=150, value=st.session_state.current_jd)
    
    if st.button("🔍 Find Matching Candidates"):
        st.session_state.current_jd = jd_input
        
        # If input is very long, it's a JD. If short, it's a query.
        if len(jd_input.split()) < 15:
            # DIRECT PYTHON MATCH (Restored Logic)
            st.session_state.shortlist = get_strict_matches(jd_input)
            st.session_state.step = "chat"
            st.rerun()
        else:
            # JD PARSING LAYER
            with st.spinner("Analyzing JD..."):
                parser = Agent(role='Parser', goal='Extract role and years.', backstory='Strict tool.', llm=groq_llm)
                task = Task(description=f"From this JD: {jd_input}, return ONLY JSON: {{\"role\": \"title\", \"years\": 5}}", expected_output="JSON", agent=parser)
                result = Crew(agents=[parser], tasks=[task]).kickoff()
                try:
                    data = json.loads(re.search(r'\{.*\}', str(result.raw), re.DOTALL).group())
                    # Convert parsed role back into a query for our strict matcher
                    query_recon = f"{data.get('role')} {data.get('years')} years"
                    st.session_state.shortlist = get_strict_matches(query_recon)
                    st.session_state.step = "chat"
                    st.rerun()
                except:
                    st.error("Extraction failed. Try a simpler search.")

# ============================================================
# PHASE 2: CHAT (MANDATORY)
# ============================================================
elif st.session_state.step == "chat":
    st.subheader("💬 Phase 2: Mandatory Candidate Interviews")
    
    if st.button("⬅️ New Search"):
        st.session_state.step = "search"
        st.session_state.shortlist = []
        st.session_state.chat_history = {}
        st.rerun()

    st.divider()

    if not st.session_state.shortlist:
        st.error(f"❌ ZERO matches for: '{st.session_state.current_jd}'. Verify role and exp in talent.json.")
    else:
        names = [p['name'] for p in st.session_state.shortlist]
        selected_name = st.radio("Select Candidate:", names, horizontal=True)

        st.info(f"Interviewing: **{selected_name}**")
        chat_container = st.container(height=350, border=True)
        
        if selected_name not in st.session_state.chat_history:
            st.session_state.chat_history[selected_name] = []

        for chat in st.session_state.chat_history[selected_name]:
            chat_container.chat_message(chat["role"]).write(chat["content"])

        if user_msg := st.chat_input(f"Message {selected_name}..."):
            st.session_state.chat_history[selected_name].append({"role": "user", "content": user_msg})
            with open('talent.json', 'r') as f:
                p_data = next((item for item in json.load(f) if item["name"] == selected_name), {})
            response = groq_llm.call([
                {"role": "system", "content": f"You are {selected_name}. Role: {p_data.get('role')}. Experience: {p_data.get('experience')}."},
                {"role": "user", "content": user_msg}
            ])
            st.session_state.chat_history[selected_name].append({"role": "assistant", "content": response})
            st.rerun()

        st.divider()
        if st.button("🎯 Proceed to Final Decision"):
            interviewed_all = all(len(st.session_state.chat_history.get(p['name'], [])) > 0 for p in st.session_state.shortlist)
            if not interviewed_all:
                st.warning("⚠️ You must interview **ALL** candidates in the list.")
            else:
                st.session_state.step = "final"
                st.rerun()

# ============================================================
# PHASE 3: FINAL VERDICT
# ============================================================
elif st.session_state.step == "final":
    st.subheader("🏆 Final Hiring Recommendation")
    if st.button("⬅️ Back to Interviews"):
        st.session_state.step = "chat"
        st.rerun()

    with st.spinner("Reviewing..."):
        director = Agent(role='Director', goal='Give verdict.', backstory='Bold.', llm=groq_llm)
        task = Task(description=f"Analyze: {json.dumps(st.session_state.chat_history)}", expected_output="Bold verdict.", agent=director)
        verdict = Crew(agents=[director], tasks=[task]).kickoff()
        st.markdown("### Decision Report")
        st.write(verdict.raw)
    
    if st.button("🔄 Start Fresh"):
        st.session_state.clear()
        st.rerun()