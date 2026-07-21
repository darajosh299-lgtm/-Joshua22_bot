# Joshua AI - Telegram Chatbot

A complete production-ready Telegram AI chatbot named **Joshua AI** built with Python, powered by the OpenAI API, and configured for seamless deployment on Railway.

---

## Features

- **Natural Responses:** Powered by OpenAI models (default: `gpt-5.5`).
- **Interactive Session Memory:** Remembers conversation history for each individual user during their session.
- **User Feedback:** Displays a live "typing..." indicator while generating replies.
- **Robust Commands:** Includes `/start`, `/help`, and `/about`.
- **Friendly Personality:** Specifically programmed to introduce its creator and assist with coding, homework, writing, translations, and business ideas.
- **Graceful Error Handling & Logging:** Clean error management to prevent sudden crashes.

---

## Project Structure

```text
telegram-ai-bot/
│
├── bot.py             # Main bot script and logic
├── requirements.txt   # Python dependencies
├── Procfile           # Process file for cloud workers
├── runtime.txt        # Python version specification
├── .env.example       # Template for environment variables
├── README.md          # Project documentation
├── .gitignore         # Files to ignore in Git
└── railway.json       # Railway deployment configurations
