# Reddit User Persona Generator

This tool generates a detailed user persona based on Reddit posts and comments using a local LLM (LLaMA3 via Ollama).

##  Requirements
- Python 3.11+
- Reddit API Credentials
- [Ollama](https://ollama.com) installed with `llama3` model pulled
- pip install -r requirements.txt

##  Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/reddit-user-persona.git
cd reddit-user-persona


## .envfile:
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_custom_user_agent

run this script
python persona_generator.py

Output
Generated persona will be saved in sample_users/<username>.txt.

Notes
	•	No OpenAI API is used – the tool uses a free offline local LLM.
	•	Ensure Ollama is running: ollama serve