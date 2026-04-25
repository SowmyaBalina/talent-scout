# AI Talent Scout - Test Scenarios

This document tests the recruiter search functionality across different input types.

## Dataset Overview
Current talent pool has 16 candidates with various roles and experience levels:
- Senior Backend Engineers: 8+ years
- Full Stack Developers: 5-9 years  
- Frontend Engineers: 5 years
- Data Scientists: 3-4 years
- DevOps Engineers: 6 years
- Mobile Developers: 7 years
- Product Designer: 4 years
- Embedded Systems Engineer: 12 years
- Junior Backend Developer: 2 years
- And more...

---

## TEST CATEGORY 1: SHORT KEYWORD SEARCHES
*Uses the strict Python filter (no LLM)*

### Test 1.1: Basic Role Keyword
**Input:** `Backend Engineer`
**Expected:** 
- bumrah (8 years, Senior Backend Engineer) ✓
- Virat kohli (8 years, Senior Backend Developer) ✓
- Sita Kumari (2 years, Junior Backend Developer) ✓

### Test 1.2: Role + Experience Requirement
**Input:** `Backend Engineer 8 years`
**Expected:**
- bumrah (8 years) ✓
- Virat kohli (8 years) ✓
- (Sita Kumari excluded - only 2 years)

### Test 1.3: Another Role Keyword
**Input:** `Data Scientist`
**Expected:**
- Sam (3 years, Data Scientist) ✓
- Marcus stonnis (4 years, Data Scientist) ✓

### Test 1.4: Role with Higher Experience Gate
**Input:** `Data Scientist 5 years`
**Expected:**
- (None - both have <5 years)

### Test 1.5: Mobile Developer
**Input:** `Mobile Developer 6 years`
**Expected:**
- Sruthi Karanam (7 years, Senior Mobile Developer) ✓

### Test 1.6: DevOps Engineer
**Input:** `DevOps Engineer`
**Expected:**
- Leo (6 years, DevOps & Platform Engineer) ✓

### Test 1.7: Designer
**Input:** `Product Designer`
**Expected:**
- Hardik Pandya (4 years, Product Designer) ✓

### Test 1.8: Full Stack
**Input:** `Full Stack Developer 5 years`
**Expected:**
- Sowmya balina (5 years, Full Stack Developer) ✓
- Himaja Halvi (9 years, Full Stack Developer) ✓

---

## TEST CATEGORY 2: LONG JD INPUTS
*Uses LLM parser to extract role & experience*

### Test 2.1: Detailed JD - Senior Backend Role
**Input:**
```
We are looking for a Senior Backend Engineer to join our scalable infrastructure team.
Requirements:
- 8+ years of backend development experience
- Expertise in Python, Django, PostgreSQL
- Experience with microservices architecture
- AWS and containerization knowledge
- Strong system design skills
Location: Remote
```
**Expected Behavior:**
- Parser extracts: Role = "Senior Backend Engineer", Years = 8
- Matches: bumrah, Virat kohli

### Test 2.2: Detailed JD - Data Science Role
**Input:**
```
We're hiring a Data Scientist for our AI/ML team.
Must have:
- 5+ years of data science experience
- Python, TensorFlow, Pandas
- Experience with ML pipelines
- SQL expertise
```
**Expected Behavior:**
- Parser extracts: Role = "Data Scientist", Years = 5
- Matches: (None - both have <5 years)

### Test 2.3: Detailed JD - DevOps/Infrastructure
**Input:**
```
DevOps Engineer needed for our cloud infrastructure team.
Looking for someone with:
- 6 years of DevOps experience minimum
- Terraform, Kubernetes, monitoring tools
- GCP or AWS expertise
- IaC best practices
```
**Expected Behavior:**
- Parser extracts: Role = "DevOps Engineer", Years = 6
- Matches: Leo (6 years)

### Test 2.4: Full Stack Developer JD
**Input:**
```
Full Stack Developer

We are looking for a talented Full Stack Developer to build our next-generation platform.

Experience Required:
- 5+ years of full-stack web development
- React, Node.js, PostgreSQL
- AWS and DevOps knowledge
- Agile experience

Nice to have:
- GraphQL
- Microservices
```
**Expected Behavior:**
- Parser extracts: Role = "Full Stack Developer", Years = 5
- Matches: Sowmya balina (5 years), Himaja Halvi (9 years)

---

## TEST CATEGORY 3: EDGE CASES & SPECIAL QUERIES

### Test 3.1: Very High Experience Requirement
**Input:** `Backend Engineer 15 years`
**Expected:** 
- (None - highest is 8 years)

### Test 3.2: Vague Query
**Input:** `Engineer`
**Expected:**
- Could match multiple roles (Backend, Senior Backend, Frontend, Mobile, etc.)
- All engineers with any experience level

### Test 3.3: Role Not in Database
**Input:** `Blockchain Developer 3 years`
**Expected:**
- (None - no blockchain developers in pool)

### Test 3.4: Just a Number
**Input:** `5 years`
**Expected:**
- Unclear - parser should handle gracefully

### Test 3.5: Multiple Keywords
**Input:** `Python Developer 5 years`
**Expected:**
- Matches candidates with "Developer" in role and 5+ years
- Could match Full Stack, Backend, Frontend

### Test 3.6: Typo/Misspelling
**Input:** `Bakcend Engineer`
**Expected:**
- No match (case-sensitive substring matching)

---

## TEST CATEGORY 4: CONVERSATIONAL QUERIES

### Test 4.1: Natural Language Query
**Input:** `Find me a Backend Engineer with 8+ years of experience`
**Expected:**
- Strips fillers: "find me", "a", "with", "+", "years", "of", "experience"
- Extracts: Role = "Backend Engineer", Experience = 8
- Matches: bumrah, Virat kohli

### Test 4.2: Casual Query
**Input:** `I want a Data Scientist`
**Expected:**
- Strips: "I", "want", "a"
- Extracts: Role = "Data Scientist"
- Matches: Sam, Marcus stonnis

### Test 4.3: Natural Language with Extras
**Input:** `Looking for a Frontend Engineer with 5+ years and React skills`
**Expected:**
- Strips fillers
- Extracts: Role = "Frontend Engineer", Experience = 5
- Matches: Smriti mandana (5 years)

### Test 4.4: Very Long Natural Query
**Input:** `I'm searching for a talented Mobile Developer who has at least 7 years of experience in iOS and Android development, preferably with Swift and Kotlin expertise`
**Expected:**
- Parser triggered (>15 words)
- Extracts: Role = "Mobile Developer", Years = 7
- Matches: Sruthi Karanam (7 years, Senior Mobile Developer)

---

## TEST CATEGORY 5: SKILL-BASED SEARCHES (Future Enhancement)

These tests show what we COULD add:

### Test 5.1: Skill Match
**Input:** `Python expert`
**Expected:** All Python developers

### Test 5.2: Tech Stack Match
**Input:** `React, TypeScript, Node.js`
**Expected:** Full stack developers with these skills

---

## HOW TO RUN THESE TESTS

1. **Start the app:**
   ```bash
   streamlit run agent.py
   ```

2. **For each test:**
   - Paste the input in the text area
   - Click "🔍 Find Matching Candidates"
   - Verify the shortlist matches expected results
   - If conversation is triggered, verify the candidates shown

3. **Document any failures:**
   - Note the input
   - Note expected vs actual results
   - Check if it's a parsing issue or matching issue

---

## SUCCESS CRITERIA

✅ **Short keywords** should use Python strict matching instantly
✅ **Long JD** should trigger LLM parsing
✅ **Experience gates** should filter out candidates below threshold
✅ **Role matching** should use substring matching
✅ **No false positives** - only qualified candidates appear

---

## NOTES

- Short queries (<15 words) use direct Python matching
- Long queries (15+ words) use LLM parser
- Experience extraction via regex looking for digits
- Role matching is case-insensitive substring matching
- Parser returns JSON with `role` and `years` fields
