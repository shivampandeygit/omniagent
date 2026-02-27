# 🤖 OmniAgent

An autonomous AI Agent with Web Search, Code Execution, Memory & ToolForge.

## Features
- 🔍 Web Search — Real-time internet search
- 🐍 Code Executor — Writes and runs Python code
- 🧠 Memory — Remembers across sessions
- 🔨 ToolForge — Creates new tools on the fly

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add `.env` file with `GROQ_API_KEY=your_key`
4. Run: `python main.py` or `streamlit run app.py`

## Tech Stack
- LLM: Groq (llama-3.3-70b)
- UI: Streamlit
- Memory: JSON-based persistent storage
