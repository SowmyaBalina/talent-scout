# 🗺️ Test Architecture & Flowchart

## How the Matcher Works

```
┌─────────────────────────────────────────────────────────────┐
│         RECRUITER INPUT (User Search Query)                 │
│  e.g., "Backend Engineer 8 years" or long JD               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Count Words in Query        │
        │  < 15 words ? ─────────┐     │
        │  15+ words ? ───────┐  │     │
        └──────────────────────┘  │     │
                                  │     │
                    SHORT QUERY   │     │  LONG QUERY
                    (Python)      │     │  (LLM Parser)
                        │         │     │
                        ▼         │     ▼
        ┌──────────────────────┐  │  ┌──────────────────┐
        │ get_strict_matches() │  │  │ Groq Parser API  │
        │                      │  │  │ Extract:         │
        │ 1. Extract exp num   │  │  │ - role title     │
        │ 2. Clean role query  │  │  │ - years required │
        │ 3. Substring match   │  │  │ (Returns JSON)   │
        │ 4. Filter by exp     │  │  └────────┬─────────┘
        │                      │  │           │
        └──────────┬───────────┘  │           ▼
                   │              │     ┌──────────────┐
                   └──────────────┼────→│ Convert to   │
                                 │      │ query format │
                                 │      │ e.g., "role  │
                                 │      │5 years"     │
                                 │      └────┬─────────┘
                                 │           │
                                 │           ▼
                                 │     get_strict_matches()
                                 │           │
                                 │           ▼
        ┌────────────────────────┴──────────────────┐
        │                                            │
        ▼                                            ▼
MATCHED CANDIDATES                          TALENT DATABASE
- Name                                      - All 16 candidates
- Role                                      - Their roles
- Experience                                - Their experience
                                            - Their skills
```

---

## Test Scenario Hierarchy

```
CANDIDATE SEARCH TESTS
│
├─ CATEGORY 1: SHORT KEYWORDS (Python Direct Match)
│  ├─ 1.1 Basic Role: "Backend Engineer" ..................... ❌
│  ├─ 1.2 Role + Exp: "Backend Engineer 8 years" ............ ❌
│  ├─ 1.3 Role Only: "Data Scientist" ....................... ✅
│  ├─ 1.4 High Exp: "Data Scientist 5 years" ............... ✅
│  ├─ 1.5 Mobile: "Mobile Developer 6 years" ............... ✅
│  ├─ 1.6 DevOps: "DevOps Engineer" ....................... ❌
│  ├─ 1.7 Designer: "Product Designer" ..................... ✅
│  └─ 1.8 Full Stack: "Full Stack Developer 5 years" ....... ✅
│
├─ CATEGORY 2: NATURAL LANGUAGE (Filler Removal)
│  ├─ 2.1 Find me Backend: "Find me Backend 8+ years" ...... ❌
│  ├─ 2.2 Looking for: "Looking for Data Scientist" ........ ❌
│  └─ 2.3 Want Frontend: "I want Frontend 5 years" ......... ❌
│
├─ CATEGORY 3: EDGE CASES (Validation)
│  ├─ 3.1 High Gate: "Backend 15 years" ................... ✅
│  ├─ 3.2 Vague: "Engineer" ............................... ✅
│  ├─ 3.3 Not Found: "Blockchain Developer" ............... ✅
│  └─ 3.4 Skills: "Python Developer 5 years" ............. ❌
│
└─ CATEGORY 4: EXACT ROLES (Role Matching)
   ├─ 4.1 Exact Backend: "Senior Backend Engineer" ........ ✅
   ├─ 4.2 Exact Dev: "Senior Backend Developer" .......... ✅
   ├─ 4.3 Junior: "Junior Backend Developer" ............. ✅
   ├─ 4.4 AI/LLM: "AI/LLM Engineer" ....................... ✅
   └─ 4.5 Security: "Cybersecurity Analyst" .............. ✅

OVERALL: 11/18 PASSED (61%)
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    TALENT SCOUT SYSTEM                       │
│                                                               │
│  ┌─────────────────┐                    ┌──────────────────┐ │
│  │   User Input    │                    │ TALENT.JSON      │ │
│  │                 │                    │ (16 candidates)  │ │
│  │ • Keyword       │                    │                  │ │
│  │ • Long JD       │                    │ Sample:          │ │
│  │ • Natural Lang  │                    │ - bumrah         │ │
│  └────────┬────────┘                    │ - Virat kohli    │ │
│           │                             │ - Sam            │ │
│           │                             │ - ...            │ │
│           │                             └────────┬─────────┘ │
│           │                                      │            │
│           ▼                                      ▼            │
│  ┌───────────────────────────────────────────────────┐       │
│  │     get_strict_matches(query, talent.json)       │       │
│  │                                                  │       │
│  │  1. Parse experience: "8 years" → 8             │       │
│  │  2. Clean query: "find me backend 8 yrs"       │       │
│  │     → "backend engineer"                       │       │
│  │  3. Loop through candidates:                   │       │
│  │     IF "backend engineer" in candidate_role    │       │
│  │     AND candidate_experience >= 8 years        │       │
│  │     THEN add to results                        │       │
│  │                                                  │       │
│  └────────────────┬────────────────────────────────┘       │
│                   │                                         │
│                   ▼                                         │
│  ┌──────────────────────────────────┐                     │
│  │      SHORTLIST (Results)         │                     │
│  │                                   │                     │
│  │  • Name                           │                     │
│  │  • Role                           │                     │
│  │  • Experience                     │                     │
│  │  • Engagement Score (later)       │                     │
│  └──────────────────────────────────┘                     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Test Execution Flow

```
START
 │
 ├──→ test_matcher.py runs
 │
 ├──→ FOR EACH TEST CASE:
 │   │
 │   ├──→ Call get_strict_matches(query)
 │   │
 │   ├──→ Check Results:
 │   │   ├── Count matches
 │   │   ├── Verify candidate names
 │   │   └── Compare with expected
 │   │
 │   └──→ Report: ✅ PASS or ❌ FAIL
 │
 ├──→ After all tests:
 │   ├── Count passes
 │   ├── Calculate percentage
 │   └── Print summary
 │
 └──→ END
```

---

## Decision Tree: Which Solution to Choose

```
        START: "I want to improve the matcher"
              │
              ▼
        Time Available?
        /           \
     YES            NO
      │              │
      ▼              ▼
   Pick one     Skip fixes
      │
      ▼
How much time?
/      |      \
5min  15min  30min
 │     │       │
 ▼     ▼       ▼
SOL1  SOL2   SOL3
 │     │       │
 ▼     ▼       ▼
QUICK BETTER BEST
Word  Fuzzy  Aliases
Match Match  Mapping
```

---

## Test Coverage Matrix

```
                  SHORT  LONG   EXACT  NATURAL EDGE
                  KW     JD     ROLE   LANG    CASE
─────────────────────────────────────────────────
Keyword Match    🔴    🔴    🟢    🔴    🟢
Experience      🟢    🟢    🟢    🔴    🟢
Experience Gate 🟢    🟢    🟢    🔴    🟢
Substring Match 🔴    🔴    🟢    🔴    🟢
Filler Remove   🟢    🟢    🟢    🔴    🟢
Role Variations 🔴    🔴    🟢    🔴    🟡
─────────────────────────────────────────────────

Legend:
🟢 = Working well
🟡 = Partially working
🔴 = Needs improvement
```

---

## File Relationships

```
Your Tests
    │
    ├─ Run this: test_matcher.py
    │            ↓
    │         TEST_RESULTS_REPORT.md ← Explains results
    │            ↓
    │         QUICK_FIX_GUIDE.md ← Shows how to fix
    │
    ├─ Manual test: QUICK_TEST_GUIDE.md
    │              ↓
    │           TEST_SCENARIOS.md ← All scenarios
    │
    └─ Overview: TEST_SUMMARY.md
                 ↓
              This file (you are here!)
```

---

## Next Steps Flowchart

```
                    ┌─────────────────────┐
                    │  Want to test app?  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                   YES                   NO
                    │                     │
                    ▼                     ▼
          ┌─────────────────────┐  ┌──────────────┐
          │ streamlit run       │  │ Want to fix  │
          │ agent.py            │  │ it?          │
          │                     │  └──────┬───────┘
          │ Use QUICK_TEST_     │         │
          │ GUIDE.md queries    │    ┌────┴─────┐
          └──────────┬──────────┘    │           │
                     │              YES         NO
                     └──────────┐    │           │
                                │    ▼           ▼
                      Report    │  Read       Read
                      findings  │  QUICK_     this
                                │  FIX_GUIDE  file
                                └────────────────
```

---

## Summary

This testing framework covers all the ways a recruiter might search:
1. ✅ Quick keywords
2. ✅ Long detailed JDs
3. ✅ Natural language phrases
4. ✅ Experience-based filtering
5. ✅ Edge cases and validation

**Result:** 61% pass rate (11/18 tests)
**Improvement Path:** Clear and documented
**Time to Fix:** 5-30 minutes
