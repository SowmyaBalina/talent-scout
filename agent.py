import streamlit as st
import json
import os
import re
from dotenv import load_dotenv
from crewai import LLM  # We keep the LLM class for the direct call

load_dotenv()

# ============================================================
# 0. CACHING FOR PERFORMANCE
# ============================================================
@st.cache_resource
def get_groq_llm():
    """Cache the Groq LLM instance to avoid reinitializing on every rerun."""
    return LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

@st.cache_data
def load_talent_pool(file_path='talent.json'):
    """Cache the talent.json data to avoid repeated file reads."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

@st.cache_data(ttl=3600)
def get_llm_response(prompt, system_content=None):
    """Cache LLM responses to avoid redundant API calls."""
    messages = []
    if system_content:
        messages.append({"role": "system", "content": system_content})
    messages.append({"role": "user", "content": prompt})
    
    groq_llm = get_groq_llm()
    return groq_llm.call(messages)

# ============================================================
# 1. THE PRECISION MATCHER (NO MISTAKES)
# ============================================================
def get_exact_matches(target_role, target_exp, file_path='talent.json'):
    pool = load_talent_pool(file_path)
    
    matches = []
    target_role = str(target_role).lower().strip()
    
    for p in pool:
        cand_role = p.get('role', '').lower()
        cand_exp_raw = str(p.get('experience', '0'))
        
        # Pull all numbers and find the highest one
        exp_nums = re.findall(r'\d+', cand_exp_raw)
        cand_exp_max = max([int(n) for n in exp_nums]) if exp_nums else 0
        
        # Logic: Role must be a substring AND experience must be >= target
        if target_role in cand_role and cand_exp_max >= target_exp:
            matches.append({"name": p['name'], "role": p['role']})
            
    return matches

# ============================================================
# 2. UI & STATE MANAGEMENT
# ============================================================
st.set_page_config(page_title="AI Talent Scout", layout="wide")

st.markdown("<h1 style='text-align: center;'>AI-Powered Talent Scouting & Engagement Agent</h1>", unsafe_allow_html=True)
st.markdown("---")

if "step" not in st.session_state: st.session_state.step = "search"
if "shortlist" not in st.session_state: st.session_state.shortlist = []
if "chat_history" not in st.session_state: st.session_state.chat_history = {}
if "current_jd" not in st.session_state: st.session_state.current_jd = ""

groq_llm = get_groq_llm()  # Use cached LLM instance

# ============================================================
# PHASE 1: DIRECT-INPUT SEARCH (RELIABLE)
# ============================================================
if st.session_state.step == "search":
    st.subheader("🕵️‍♂️ Phase 1: Precise Sourcing")
    jd_input = st.text_area("Enter JD or Search Phrase:", height=250, value=st.session_state.current_jd)
    
    if st.button("🔍 Find Matching Candidates"):
        if not jd_input.strip():
            st.warning("Please enter something to search.")
        else:
            # WIPE STATE IMMEDIATELY
            st.session_state.shortlist = []
            st.session_state.chat_history = {}
            st.session_state.current_jd = jd_input
            
            with st.spinner("🔍 System is extracting requirements..."):
                # Use a Direct LLM Call - MUCH more reliable than an Agent for parsing
                prompt = (
                    f"Extract the Job Title and Minimum Years of Experience from this text: '{jd_input}'. "
                    "Return ONLY a JSON object like this: {'role': 'backend engineer', 'years': 5}. "
                    "If no years are mentioned, use 0. Return ONLY the JSON."
                )
                
                try:
                    # Direct call to bypass CrewAI "Agent" overhead errors
                    response = get_llm_response(prompt)
                    
                    # Robust Regex to find JSON
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group())
                        r_req = data.get('role', '')
                        y_req = int(data.get('years', 0))
                        
                        # Execute Match
                        st.session_state.shortlist = get_exact_matches(r_req, y_req)
                        st.session_state.step = "chat"
                        st.rerun()
                    else:
                        st.error("Could not determine role/experience. Try: 'Product Designer 5 years'")
                except Exception as e:
                    st.error(f"Search failed. Error: {e}")

# ============================================================
# PHASE 2: INTERVIEWS (STABLE)
# ============================================================
elif st.session_state.step == "chat":
    st.subheader("💬 Phase 2: Candidate Engagement")
    if st.button("⬅️ New Search"):
        st.session_state.step = "search"
        st.rerun()

    if not st.session_state.shortlist:
        st.error("❌ No candidates found matching those exact requirements.")
    else:
        names = [p['name'] for p in st.session_state.shortlist]
        sel = st.radio("Select Candidate:", names, horizontal=True)

        st.info(f"Chatting with: **{sel}**")
        chat_box = st.container(height=400, border=True)
        
        if sel not in st.session_state.chat_history:
            st.session_state.chat_history[sel] = []

        for chat in st.session_state.chat_history[sel]:
            chat_box.chat_message(chat["role"]).write(chat["content"])

        if msg := st.chat_input(f"Message {sel}..."):
            st.session_state.chat_history[sel].append({"role": "user", "content": msg})
            
            talent_pool = load_talent_pool('talent.json')
            c_data = next((i for i in talent_pool if i["name"] == sel), {})
            
            ans = get_llm_response(
                prompt=msg,
                system_content=f"You are {sel}. Role: {c_data.get('role')}."
            )
            st.session_state.chat_history[sel].append({"role": "assistant", "content": ans})
            st.rerun()

        st.divider()
        if st.button("🎯 Proceed to Verdict"):
            messaged_all = all(len(st.session_state.chat_history.get(n, [])) > 0 for n in names)
            if not messaged_all:
                st.warning("You must message every candidate first.")
            else:
                st.session_state.step = "final"
                st.rerun()

# ============================================================
# PHASE 3: FINAL VERDICT
# ============================================================
elif st.session_state.step == "final":
    st.subheader("🏆 Final Decision")
    if st.button("⬅️ Back"):
        st.session_state.step = "chat"
        st.rerun()
    
    with st.spinner("Reviewing..."):
        # We can use a simple LLM call here too for speed
        eval_prompt = f"Review these interviews: {json.dumps(st.session_state.chat_history)}. Give a bold Hire/Reject verdict for each."
        verdict = get_llm_response(eval_prompt)
        st.markdown(verdict)
    
    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()