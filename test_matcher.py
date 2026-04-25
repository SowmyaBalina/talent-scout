#!/usr/bin/env python3
"""
Automated Test Runner for AI Talent Scout
Tests the get_strict_matches() function with various inputs
"""

import json
import os
import re

def get_strict_matches(query, file_path='talent.json'):
    """
    STRICT RULE: 
    1. Extracts numerical experience (e.g., '8' from '8 years').
    2. Identifies the exact role phrase (e.g., 'product designer').
    3. Matches ONLY if the role name exists and experience is >= requirement.
    """
    if not os.path.exists(file_path):
        return []
        
    with open(file_path, 'r') as f:
        pool = json.load(f)
    
    query_lower = query.lower()
    
    # Extract Minimum Experience (e.g., '10' from '10+ years')
    numbers = re.findall(r'\d+', query_lower)
    required_exp = int(numbers[0]) if numbers else 0
    
    # CLEAN THE QUERY: Remove fillers but KEEP the core role
    clean_role = query_lower
    fillers = ["find me a", "find me", "search for", "give me", "i want", "looking for", "with", "experience", "years", "exp", "yrs"]
    for word in fillers:
        clean_role = clean_role.replace(word, "")
    
    # Remove any remaining numbers and extra spaces
    clean_role = re.sub(r'\d+', '', clean_role).strip(",. ")

    matches = []
    for p in pool:
        cand_role = p.get('role', '').lower()
        
        # Extract candidate's numeric experience
        cand_exp_raw = str(p.get('experience', '0'))
        cand_exp_match = re.search(r'\d+', cand_exp_raw)
        cand_exp_num = int(cand_exp_match.group()) if cand_exp_match else 0
        
        # --- THE STRICT GATE ---
        if clean_role in cand_role and cand_exp_num >= required_exp:
            matches.append({"name": p['name'], "role": p['role'], "experience": p['experience']})
            
    return matches

# ============================================================
# TEST SUITE
# ============================================================

def run_test(test_name, query, expected_count=None, expected_names=None, should_fail=False):
    """Run a single test and report results"""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"INPUT: '{query}'")
    print(f"{'='*70}")
    
    results = get_strict_matches(query)
    
    print(f"RESULTS: {len(results)} match(es)")
    for candidate in results:
        print(f"  ✓ {candidate['name']:20} | {candidate['role']:30} | {candidate['experience']}")
    
    # Validate
    success = True
    if expected_count is not None:
        if len(results) == expected_count:
            print(f"✅ COUNT CHECK PASSED: Found {expected_count} matches")
        else:
            print(f"❌ COUNT CHECK FAILED: Expected {expected_count}, got {len(results)}")
            success = False
    
    if expected_names:
        found_names = [r['name'] for r in results]
        for name in expected_names:
            if name in found_names:
                print(f"✅ FOUND: {name}")
            else:
                print(f"❌ MISSING: {name}")
                success = False
    
    if should_fail and len(results) == 0:
        print(f"✅ CORRECTLY RETURNED NO RESULTS")
    elif should_fail and len(results) > 0:
        print(f"❌ SHOULD HAVE RETURNED NO RESULTS")
        success = False
    
    return success

# ============================================================
# RUN ALL TESTS
# ============================================================

print("\n" + "="*70)
print("AI TALENT SCOUT - AUTOMATED TEST SUITE")
print("="*70)

results = []

# CATEGORY 1: SHORT KEYWORD SEARCHES
print("\n\n📌 CATEGORY 1: SHORT KEYWORD QUERIES")

results.append(run_test(
    "1.1 - Basic Role Keyword",
    "Backend Engineer",
    expected_count=3,
    expected_names=["bumrah", "Virat kohli", "Sita Kumari"]
))

results.append(run_test(
    "1.2 - Role + Experience Gate",
    "Backend Engineer 8 years",
    expected_count=2,
    expected_names=["bumrah", "Virat kohli"]
))

results.append(run_test(
    "1.3 - Data Scientist",
    "Data Scientist",
    expected_count=2,
    expected_names=["Sam", "Marcus stonnis"]
))

results.append(run_test(
    "1.4 - Data Scientist 5 years (no match)",
    "Data Scientist 5 years",
    expected_count=0,
    should_fail=True
))

results.append(run_test(
    "1.5 - Mobile Developer",
    "Mobile Developer 6 years",
    expected_count=1,
    expected_names=["Sruthi Karanam"]
))

results.append(run_test(
    "1.6 - DevOps Engineer",
    "DevOps Engineer",
    expected_count=1,
    expected_names=["Leo"]
))

results.append(run_test(
    "1.7 - Product Designer",
    "Product Designer",
    expected_count=1,
    expected_names=["Hardik Pandya"]
))

results.append(run_test(
    "1.8 - Full Stack Developer",
    "Full Stack Developer 5 years",
    expected_count=2,
    expected_names=["Sowmya balina", "Himaja Halvi"]
))

# CATEGORY 2: NATURAL LANGUAGE QUERIES
print("\n\n🗣️ CATEGORY 2: NATURAL LANGUAGE QUERIES")

results.append(run_test(
    "2.1 - Natural: Find me Backend Engineer",
    "Find me a Backend Engineer with 8+ years",
    expected_count=2,
    expected_names=["bumrah", "Virat kohli"]
))

results.append(run_test(
    "2.2 - Natural: I want Data Scientist",
    "Looking for a Data Scientist",
    expected_count=2,
    expected_names=["Sam", "Marcus stonnis"]
))

results.append(run_test(
    "2.3 - Natural: Frontend Engineer",
    "I want a Frontend Engineer with 5 years",
    expected_count=1,
    expected_names=["Smriti mandana"]
))

# CATEGORY 3: EDGE CASES
print("\n\n⚠️ CATEGORY 3: EDGE CASES")

results.append(run_test(
    "3.1 - Very High Experience Gate",
    "Backend Engineer 15 years",
    expected_count=0,
    should_fail=True
))

results.append(run_test(
    "3.2 - Vague Query (just 'Engineer')",
    "Engineer",
    expected_count=None  # Multiple matches expected
))

results.append(run_test(
    "3.3 - Role Not in Database",
    "Blockchain Developer",
    expected_count=0,
    should_fail=True
))

results.append(run_test(
    "3.4 - Multiple Keywords",
    "Python Developer 5 years",
    expected_count=None  # Should match developers with 5+ years
))

# CATEGORY 4: EXACT ROLE MATCHES
print("\n\n🎯 CATEGORY 4: EXACT ROLE SEARCHES")

results.append(run_test(
    "4.1 - Exact: Senior Backend Engineer",
    "Senior Backend Engineer",
    expected_count=1,
    expected_names=["bumrah"]
))

results.append(run_test(
    "4.2 - Exact: Senior Backend Developer",
    "Senior Backend Developer",
    expected_count=1,
    expected_names=["Virat kohli"]
))

results.append(run_test(
    "4.3 - Exact: Junior Backend Developer",
    "Junior Backend Developer",
    expected_count=1,
    expected_names=["Sita Kumari"]
))

results.append(run_test(
    "4.4 - Exact: AI/LLM Engineer",
    "AI/LLM Engineer",
    expected_count=1,
    expected_names=["Sai Teja"]
))

results.append(run_test(
    "4.5 - Exact: Cybersecurity Analyst",
    "Cybersecurity Analyst",
    expected_count=1,
    expected_names=["Supreetha Sharma"]
))

# FINAL REPORT
print("\n\n" + "="*70)
print("TEST SUITE SUMMARY")
print("="*70)

passed = sum(results)
total = len(results)
percentage = (passed / total * 100) if total > 0 else 0

print(f"\nTests Passed: {passed}/{total} ({percentage:.1f}%)")

if passed == total:
    print("\n✅ ALL TESTS PASSED! The matcher is working correctly.")
else:
    print(f"\n⚠️  {total - passed} test(s) failed. Review the output above.")

print("\n" + "="*70)
