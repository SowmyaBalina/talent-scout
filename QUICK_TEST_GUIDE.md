# Quick Test Reference - Copy & Paste These

## 🎯 QUICK TESTS - Copy each input below into the app

---

### CATEGORY 1: SHORT KEYWORD QUERIES (Instant Python Match)
```
Backend Engineer
```
✓ Expected: bumrah, Virat kohli, Sita Kumari

---

```
Backend Engineer 8 years
```
✓ Expected: bumrah, Virat kohli (Sita excluded - only 2 years)

---

```
Data Scientist
```
✓ Expected: Sam, Marcus stonnis

---

```
Mobile Developer 6 years
```
✓ Expected: Sruthi Karanam (7 years)

---

```
DevOps Engineer
```
✓ Expected: Leo

---

```
Full Stack Developer 5 years
```
✓ Expected: Sowmya balina, Himaja Halvi

---

```
Product Designer
```
✓ Expected: Hardik Pandya

---

### CATEGORY 2: NATURAL LANGUAGE QUERIES (Short)
```
Find me a Backend Engineer with 8+ years
```
✓ Expected: bumrah, Virat kohli

---

```
Looking for a Data Scientist
```
✓ Expected: Sam, Marcus stonnis

---

```
I want a Frontend Engineer with 5 years
```
✓ Expected: Smriti mandana

---

### CATEGORY 3: LONG JD INPUTS (LLM Parser)
```
We are looking for a Senior Backend Engineer to join our team.
Requirements:
- 8+ years of backend development
- Python, Django, PostgreSQL expertise
- Microservices architecture knowledge
- AWS experience
Location: Remote
```
✓ Expected: bumrah, Virat kohli

---

```
Data Scientist position available.

Requirements:
- 5+ years of experience
- Python, TensorFlow, SQL
- ML pipeline expertise
- Strong statistical background
```
✓ Expected: (None - both candidates have <5 years)

---

```
DevOps Engineer

We need someone with:
- 6 years minimum DevOps experience
- Terraform, Kubernetes
- GCP or AWS
- Infrastructure-as-Code
```
✓ Expected: Leo

---

```
Full Stack Developer

5+ years required. Tech stack: React, Node.js, PostgreSQL, AWS.
Build scalable web applications.
```
✓ Expected: Sowmya balina, Himaja Halvi

---

### CATEGORY 4: EDGE CASES
```
Backend Engineer 15 years
```
✓ Expected: (None - no one has 15+ years)

---

```
Engineer
```
✓ Expected: All engineers (Backend, Frontend, DevOps, Mobile, etc.)

---

```
Blockchain Developer
```
✓ Expected: (None - not in database)

---

### CATEGORY 5: MULTI-SKILL NATURAL QUERIES
```
I'm looking for a talented Mobile Developer with at least 7 years of iOS and Android experience, preferably Swift and Kotlin expertise
```
✓ Expected: Sruthi Karanam (7 years, Senior Mobile Developer)

---

```
Hiring: Senior Backend Engineer with 8+ years Python/Django/PostgreSQL and microservices experience. Remote role available.
```
✓ Expected: bumrah, Virat kohli

---

## 📊 RESULT SUMMARY TABLE

| Test Input | Input Type | Expected Match | Should Pass |
|-----------|-----------|-----------------|-----------|
| `Backend Engineer` | Keyword | 3 results | ✓ |
| `Backend Engineer 8 years` | Keyword + Exp | 2 results | ✓ |
| `Find me Backend Engineer 8+` | Natural | 2 results | ✓ |
| Data Scientist JD (long) | LLM Parse | 0 results | ✓ |
| `Blockchain Developer` | Not in DB | 0 results | ✓ |
| `Engineer` (vague) | Keyword | Multiple | ✓ |
| `Backend Engineer 15 years` | High exp gate | 0 results | ✓ |

---

## 🔍 HOW TESTING WORKS

**Short Input (<15 words)**
- Uses: Direct Python regex matching
- Speed: Instant
- Accuracy: Strict substring matching

**Long Input (15+ words)**  
- Uses: Groq LLM parser
- Speed: 2-3 seconds
- Accuracy: Semantic understanding

---

## 🚀 RUN THE APP

```bash
cd c:\Users\sowmy\OneDrive\Desktop\Talent-scout
streamlit run agent.py
```

Then copy-paste each test input and verify results!
