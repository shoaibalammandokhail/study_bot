AI Study Assistant with Memory (FastAPI + Groq + MongoDB)
Project Overview

This project is an AI-powered Study Assistant built using FastAPI and Groq LLM.
The chatbot answers academic-related questions and stores conversation history using MongoDB for contextual memory.

"I use Railway for Deployment"

The API is deployed on Railway.
Technologies Used
FastAPI
Groq LLM (openai/gpt-oss-20b)
MongoDB
Railway (Cloud Deployment)
Python
Memory Implementation

The chatbot retrieves the last 5 previous messages of a user from MongoDB and sends them as context to the LLM.

previous_chats = collection.find(
    {"user_id": request.user_id}
).sort("_id", -1).limit(5)

This allows context-based conversation per user.

API Endpoints
POST /chat
Hosted API

Railway link here
Example:
https://studybot-production-4e34.up.railway.app/docs

GitHub Repo
https://github.com/shoaibalammandokhail/study_bot.git

Setup Instructions (Local)
Clone repository

Features
✔ Academic-only chatbot
✔ Context memory using MongoDB
✔ Cloud deployment
✔ REST API
✔ Production-ready structure
