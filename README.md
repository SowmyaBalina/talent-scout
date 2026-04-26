AI-Powered Talent Scouting & Recruitment Agent 🕵️‍♂️⚡
An intelligent recruitment system designed to revolutionize candidate sourcing. It combines fast Python-based matching for quick searches with Groq's LLM for parsing complex job descriptions, enabling recruiters to find perfect talent matches in seconds.

🚀 Project Overview
Traditional recruitment involves hours of manual profile sifting. This project automates candidate sourcing by:

✅ **Instant Matching** - Quick keyword searches return candidates instantly
✅ **Natural Language Processing** - Understands recruiter queries like "find me a full stack developer with 5 years of experience"
✅ **JD Parsing** - Automatically extracts role requirements from long job descriptions using Groq LLM
✅ **Smart Experience Filtering** - Ensures candidates have >= required years (not less)
✅ **Role Variation Handling** - Matches "Backend Engineer" with "Backend Developer", "Senior Backend Engineer", etc.

🛠️ Tech Stack
- **Fast Matcher:** Python regex + keyword-based matching (instant results)
- **LLM Engine:** Groq Cloud with Llama 3.3 (for JD parsing)
- **Framework:** Streamlit (interactive UI)
- **Data Format:** JSON-based Talent Database for time being ,we can use supabase for larger databases f
- **Language:** Python 3.12+

🧠 How It Works
The system uses a **dual-approach matching strategy** with a **3-phase recruitment workflow**:

## Phase 1️⃣: Precise Sourcing (Candidate Search)
1. **Short Queries (< 15 words):** Python-based matcher
   - "Full Stack Developer 5 years" → Instant results
   - Uses keyword extraction and experience filtering
   - No LLM needed (faster, cheaper)

2. **Long Queries (15+ words):** LLM-powered parser
   - Complex job descriptions
   - Groq extracts role requirements automatically
   - Falls back to Python matcher for results

## Phase 2️⃣: Mandatory Candidate Interviews (Engagement)
- Recruiter interviews **each candidate individually**
- Real-time chat with AI-simulated candidates
- Candidates respond based on their background and outreach history
- Collects candidate sentiment and interest signals
- **All candidates must be interviewed before proceeding**

## Phase 3️⃣: Final Hiring Recommendation (Decision)
- AI Director analyzes all interview conversations
- Evaluates:
  - Technical fit (experience + skills match)
  - Cultural fit (responses + sentiment)
  - Genuine interest (engagement level)
  - Availability (start date readiness)
- Provides bold hiring recommendation with reasoning
- Ranks candidates for final selection

**Matching Algorithm (Phase 1):**
- Extracts minimum experience requirement from query
- Breaks down role query into keywords (handles natural language)
- Filters candidates where: ALL keywords in role AND experience >= requirement
- Returns ranked matches

📋 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd Talent-scout
```

### 2. Install Dependencies
```bash
pip install crewai streamlit python-dotenv litellm
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 4. Prepare Data
Ensure `talent.json` is in the root directory with this format:
```json
[
  {
    "name": "Sowmya balina",
    "role": "Full Stack Developer",
    "skills": ["Python", "React", "AWS"],
    "experience": "5 years",
    "last_outreach_response": "Looking for a new challenge..."
  }
]
```
🚀 Usage

### Complete Workflow

The recruitment process happens in **3 phases**:

#### Phase 1️⃣ - Candidate Search
```bash
streamlit run agent.py
```

1. Enter a recruiter search query:
   - Short: `"Full Stack Developer 5 years"`
   - Long: Paste a detailed job description
2. Click **"🔍 Find Matching Candidates"**
3. System returns ranked matching candidates

#### Phase 2️⃣ - Interview Each Candidate
1. System shows all matched candidates
2. Select a candidate from the radio button
3. Chat with them to assess:
   - Interest level in the role
   - Salary expectations
   - Availability
   - Specific concerns
4. **Repeat for all candidates** (mandatory)
5. Click **"🎯 Proceed to Final Decision"** when done

#### Phase 3️⃣ - AI Director's Final Decision
1. System analyzes all interview conversations
2. AI Director evaluates:
   - Technical match (skills + experience)
   - Interest signals (engagement in chat)
   - Genuine intent (responses quality)
   - Availability (can start soon?)
3. Provides **final hiring recommendation**
4. Shows ranked candidates with reasoning

### Example Recruiter Searches
- `"Full Stack Developer"` → Finds all full stack developers instantly
- `"Backend Engineer 8 years"` → Finds backend engineers with 8+ years
- `"Find me a Data Scientist with 5 years of experience"` → Natural language query
- Long JD with full job description → LLM parses and finds matches

🧪 Testing

### Run Automated Tests
```bash
python test_matcher.py
```

This runs 18 comprehensive test cases covering:
- ✅ Short keyword searches
- ✅ Long JD inputs
- ✅ Natural language queries
- ✅ Experience-based filtering
- ✅ Edge cases

### Manual Testing
Copy queries from `QUICK_TEST_GUIDE.md` and test in the app.

### Test Documentation
- `TEST_SUMMARY.md` - Quick overview of test results
- `TEST_SCENARIOS.md` - Detailed test cases
- `TEST_RESULTS_REPORT.md` - Analysis and recommendations
- `QUICK_TEST_GUIDE.md` - Ready-to-use test queries
- `QUICK_FIX_GUIDE.md` - Improvement recommendations

📊 Current Test Results
- **Tests Passing:** 11/18 (61%)
- **Exact Role Matches:** ✅ 100%
- **Experience Filtering:** ✅ 100%
- **Natural Language:** ⚠️ Improved in latest version

🔑 Key Features

### 1. Smart Keyword Matching
```
Query: "full stack developer"
Matches: ✅ Full Stack Developer
         ✅ Senior Full Stack Developer  
         ✅ Full Stack Engineer
Does NOT match: ❌ Frontend Developer (missing "stack" keyword)
```

### 2. Experience Requirements
```
Query: "5 years"
Matches: ✅ Candidates with 5, 6, 7, 8... years
Does NOT match: ❌ Candidates with 3, 4 years (less than 5)
```

### 3. Natural Language Support
```
Supported queries:
- "Find me a Backend Engineer"
- "Looking for a Data Scientist with 5 years"
- "I want a Full Stack Developer with 8+ years of experience"
- Long detailed job descriptions
```

📈 Performance
- **Fast Queries:** <100ms (Python matcher)
- **LLM Queries:** 2-5 seconds (Groq parsing)
- **Rate Limiting:** Automatic retry with exponential backoff
- **No Downtime:** Graceful error handling

�️ Architecture

```
User Query
    ↓
Word Count Check (<15 or 15+?)
    ├─ Short (< 15 words) → Python Matcher (FAST)
    │  ├─ Extract experience requirement
    │  ├─ Extract role keywords
    │  ├─ Filter & match candidates
    │  └─ Return instantly
    │
    └─ Long (15+ words) → Groq LLM Parser
       ├─ Send to Groq API
       ├─ Extract role & years
       ├─ Convert to standard format
       └─ Pass to Python matcher

Results
    ↓
Ranked Candidates
```

📚 File Structure
```
Talent-scout/
├── agent.py                    # Main application
├── talent.json                 # Candidate database
├── test_matcher.py             # Automated test suite
├── README.md                   # This file
├── TEST_SUMMARY.md             # Test overview
├── TEST_SCENARIOS.md           # Detailed test cases
├── TEST_RESULTS_REPORT.md      # Analysis & recommendations
├── QUICK_TEST_GUIDE.md         # Copy-paste test queries
├── QUICK_FIX_GUIDE.md          # Improvement guide
└── TEST_ARCHITECTURE.md        # Architecture diagrams
```

🧪 Testing Steps Performed

✅ **Keyword Matching Test**
- Query: "Backend Engineer"
- Expected: Matches both "Senior Backend Engineer" and variations
- Result: Working with improved keyword extraction

✅ **Experience Filtering Test**
- Query: "5 years"
- Expected: Only candidates with 5+ years
- Result: Correctly filters by >= requirement

✅ **Natural Language Test**
- Query: "Find me a full stack developer with 5 years of experience"
- Expected: Extracts role and experience, returns matches
- Result: Improved with new filler word removal

✅ **Performance Test**
- Short queries: <100ms (Python only)
- Long JDs: 2-5 seconds (with Groq parsing)
- Rate limiting: Automatic retry with exponential backoff

📈 Future Roadmap

1. **Skill-Based Matching** - Search by specific technologies (Python, React, AWS, etc.)
2. **Vector Embeddings** - Semantic similarity for better matching
3. **Candidate Ranking** - Multi-factor scoring (skills + experience + interest)
4. **LinkedIn Integration** - Live candidate data
5. **Engagement Tracking** - Outreach history and sentiment analysis
6. **Batch Processing** - Process multiple candidates at once

🤝 Contributing
Feel free to submit issues and enhancement requests!

👤 About
Built with ❤️ for fast, intelligent talent sourcing.
Version: 2.0 (Improved matcher with natural language support)
Last Updated: April 25, 2026

📝 License
MIT License - Feel free to use this project for your recruitment needs!

🎯 Key Improvements in v2.0
- ✅ Better natural language handling
- ✅ Keyword-based role matching (fixes Engineer/Developer confusion)
- ✅ Proper experience filtering (>= not just ==)
- ✅ Filler word removal for recruiter phrases
- ✅ Comprehensive test suite (18 test cases)
- ✅ Automatic rate limit handling with Groq


Updates and changes I made while testing manually - 
1.I made sure that recruiter should mandatorily interview the candidates and then only it should proceed with the final decision ,added that validation. 
2. I implemented Strict Role Scoping. If a recruiter asks for an "Engineer," the system now distinguishes it from a "Developer." I forced the code to treat the role as a specific identity, not just a list of skills.
3. I combined the flexibility of LLMs with the reliability of strict Python logic.
