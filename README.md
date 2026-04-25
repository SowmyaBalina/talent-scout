AI-Powered Talent Scouting & Engagement Agent 🕵️‍♂️⚡
An autonomous multi-agent system designed to revolutionize the recruitment process. By leveraging Groq’s LPU™ (Language Processing Unit) and Llama 3.3, this agent analyzes candidate pools in seconds to find the best technical and cultural fits.

🚀 Project Overview
Traditional recruitment involves hours of manual profile sifting. This project automates that "top-of-funnel" work by using AI agents to:

Parse complex Job Descriptions (JDs).

Match candidates based on semantic skill alignment (not just keywords).

Analyze candidate sentiment from outreach logs to gauge genuine interest.

Rank talent with dual-scoring: Match Score and Interest Score.

🛠️ Tech Stack
Inference Engine: Groq Cloud (Ultra-fast LLM inference)

Model: Meta Llama-3.3-70b-Versatile

Orchestration: CrewAI (Autonomous Multi-Agent Framework)

Frontend: Streamlit

Data Source: JSON-based Talent Database

Language: Python 3.12+

🧠 System Architecture
The system uses a sequential multi-agent workflow:

Technical Matcher Agent: Analyzes the JD requirements against the skills and experience fields in the talent pool.

Engagement Analyst Agent: Reviews the last_outreach_response field using sentiment analysis to determine if the candidate is actively looking or passive.

📋 Installation & Setup
1. Clone the Repository
Bash
git clone <your-repository-url>
cd Talent-scout
2. Install Dependencies
Bash
pip install crewai litellm langchain-groq streamlit python-dotenv
3. Configure Environment Variables
Create a .env file in the root directory and add your Groq API Key:

Plaintext
GROQ_API_KEY=gsk_your_actual_key_here
4. Prepare the Data
Ensure your talent.json file is in the root directory. The system expects the following format:

JSON
[
  {
    "name": "Jordan Smith",
    "skills": ["Python", "Django", "PostgreSQL"],
    "experience": "8 years of backend development",
    "last_outreach_response": "I am open to discussing senior roles."
  }
]
🚀 Execution
To launch the agent, run:

Bash
python -m streamlit run agent.py
🧪 Testing Steps Performed
Skill Match Test: Inputted a "Python Developer" JD. The agent correctly ranked candidates with Python/Django experience higher than Frontend developers.

Sentiment/Interest Test: Inputted candidates who were "Happy in current role" vs "Actively looking." The agent successfully assigned lower Interest Scores to passive candidates despite high technical skill matches.

Performance Test: Leveraged Groq to reduce agent "thinking time" from 60+ seconds (standard cloud LLMs) to under 10 seconds.

Error Handling: Implemented max_rpm and max_iter limits to manage API quotas and prevent infinite agent loops.

📈 Future Roadmap
Vector Database Migration: Transitioning from JSON to Supabase (PostgreSQL) for vector similarity searches.

LinkedIn Integration: Scraping live data to replace static JSON files.

Voice Outreach: Integrating ElevenLabs to allow the agent to perform initial screening calls.

👤 Author
Name: [Your Name]

Role: AI Engineer / Hackathon Participant

GitHub: [Your GitHub Link]

💡 Final Tips for your GitHub
Rename your Repo: Make sure the name is something like ai-talent-scout-agent.

Add a License: Use the MIT License (it's standard for hackathons).

The "About" Section: Use the description: "A high-speed recruitment agent using Groq and CrewAI to automate candidate matching and sentiment analysis."