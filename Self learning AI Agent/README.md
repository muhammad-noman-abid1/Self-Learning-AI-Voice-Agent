# Self Learning - Personal AI Assistant

> A Self Learning personal AI assistant built with Python, featuring long-term memory, web search, and voice interaction.


## Overview

This project is a **Self Learning personal AI assistant** built from scratch with Python.

The main objective is to understand how modern AI applications can combine:

- Long-term memory
- Web search
- Large Language Models
- Speech recognition
- Text-to-speech
- Modular Python components

Unlike a simple chatbot, the assistant can remember important personal information about the user and retrieve those memories when they are relevant to a conversation.

The project is primarily designed as a **learning and experimentation project** for understanding AI assistant architecture and integrating multiple AI technologies into one application.

---

# Features

### Long-Term Memory

The assistant can identify important personal information and store it as long-term memory.

Examples include:

- User's preferred name
- Likes and dislikes
- Personal preferences
- Education
- Work information
- Long-term interests
- Stable personal facts

Memory is stored using **Mem0** with **Qdrant** as the local vector database.

The assistant does **not** attempt to store every conversation.

---

### Current Web Information

The assistant can determine whether a question requires current information from the Internet.

When necessary, it uses **Tavily** to search the web and provide the retrieved information to the language model.

This allows the assistant to handle questions involving:

- Latest news
- Current events
- Current information
- Weather
- Current prices
- Other frequently changing information

Search sources are also displayed in the terminal when web search is used.

---

### Voice Interaction

The assistant supports hands-free voice interaction.

The current voice workflow is:

```text
Microphone
     ↓
Speech Recognition
     ↓
"Nom Nom"
     ↓
"Yes sir, Nomi."
     ↓
User Command
     ↓
AI Assistant
     ↓
Text-to-Speech
     ↓
Speaker.
```
---

## Architecture

```text
User
  ↓
Voice Input
  ↓
Memory Check
  ↓
Long-Term Memory (Mem0 + Qdrant)
  ↓
Web Search Check
  ↓
Tavily Web Search (if needed)
  ↓
Groq LLM
  ↓
AI Response
  ↓
Voice Output
```
---

## Project Structure

Self learning AI Agent/
│
├── README.md
├── requirements.txt
├── .gitignore
│
└── src/
    ├── main.py
    ├── memory_decision.py
    ├── memory_extraction.py
    ├── web_decision.py
    ├── web_search.py
    ├── voice_input.py
    └── voice_output.py