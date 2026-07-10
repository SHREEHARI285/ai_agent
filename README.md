# AI Agent with Tools 🤖

An AI agent powered by Gemini that reasons about which tool to use 
to answer complex questions.

## Live Demo
🔗 [https://aiagent-hari.streamlit.app/]

## Tools Available
- 🧮 **Calculator** — math expressions
- 🔍 **Web Search** — current news via DuckDuckGo  
- 📖 **Wikipedia** — facts and general knowledge

## How It Works
The agent uses chain-of-thought reasoning to decide which tool fits 
each question, calls it, reads the result, and formulates a final answer.

## Tech Stack
- LangChain 1.3+ with create_agent API
- Gemini API
- DuckDuckGo Search
- Wikipedia API
- Streamlit

## Setup
```bash
git clone https://github.com/yourusername/ai-agent
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your-key" > .env
streamlit run deploy_app.py
```
