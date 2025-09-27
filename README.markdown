# Christopher Nolan Scriptwriter Bot

## 📋 Project Overview

This Telegram bot acts as a scriptwriting assistant inspired by Christopher Nolan. Powered by Yandex GPT, it helps users generate stories in various genres with customizable characters and settings. Users can start, continue, or end stories, view full narratives, and track token usage. It's designed for creative writing enthusiasts and demonstrates AI integration in bot development.

### 🎯 Key Objectives
- Generate engaging story fragments or complete narratives.
- Manage user sessions and token limits for sustainable usage.
- Provide an intuitive interface with keyboard buttons.
- Log activities for debugging and monitoring.

## 🛠️ Tech Stack

| Category          | Tools/Technologies       | Purpose |
|-------------------|--------------------------|---------|
| **Bot Framework** | pyTelegramBotAPI        | Telegram bot handling |
| **AI Integration**| Yandex GPT              | Story generation |
| **Database**      | SQLite                  | User and story data storage |
| **HTTP Requests** | Requests                | API calls to Yandex |
| **Language**      | Python 3.9+             | Core scripting |
| **Logging**       | Python logging          | Error and activity tracking |

## 🏗️ Architecture

1. **User Interaction**: Commands and buttons trigger story setup and generation.
2. **Story Settings**: Users select genre, character, setting, and add info.
3. **GPT Generation**: Yandex GPT creates story parts based on prompts.
4. **Database Storage**: Tracks users, sessions, tokens, and story history.
5. **Token Management**: Enforces limits to prevent overuse.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Telegram Bot Token and Yandex GPT credentials

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TsMark01/bot_scenarist.git
   cd bot_scenarist
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Secrets**
   - Edit `info.py` with your `tg`, `folder`, and `iam`.

4. **Run the Bot**
   ```bash
   python bot.py
   ```

### Usage Commands
- `/start`: Welcome and start interaction.
- `/help`: Show instructions.
- `/story` or `/newstory`: Begin a new story.
- `/begin`: Generate story start.
- `/continue`: Add to the story.
- `/end`: Finish the story.
- `/wholestory`: View full story.
- `/tokens`: Check remaining sessions/tokens.
- `/debug`: Get error logs.

## 📊 Features

- **Customizable Stories**: Choose genre, character, setting, and extras.
- **Session Limits**: Max users, sessions, and tokens per session.
- **Button Navigation**: Easy keyboards for selections.
- **Logging**: Detailed activity and error logs.

## 🧪 Testing

- Interact via Telegram commands/buttons.
- Check logs for errors: `cat log_file.txt`.
- Verify token deductions and story history in `db.hope`.

## 🔮 Future Enhancements

- Add more genres/characters/settings.
- Integrate title generation.
- Support multi-user collaboration.

---
Built by Mark Tsyrul, it was the final project of the third part of Yandex Course
