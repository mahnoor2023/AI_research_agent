# AI Research Agent

Single-agent research app: CrewAI + Groq (`openai/gpt-oss-120b`) + DuckDuckGo search + Streamlit.

## Deploy (no local setup needed)
1. Get a free key at https://console.groq.com -> API Keys.
2. Upload all these files to a GitHub repo (keep the file names as they are).
3. Go to https://share.streamlit.io -> Create app -> pick your repo, branch `main`, main file `app.py`.
4. Click **Advanced settings**:
   - Python version: **3.12**
   - Secrets box:
     ```toml
     GROQ_API_KEY = "your_real_key"
     ```
5. Click **Deploy**.

To change the key later: App -> Settings -> Secrets.
