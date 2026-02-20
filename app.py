from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Get environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")


# LLM Setup
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="openai/gpt-oss-20b",  # your requested model
)

# MongoDB Setup
client = MongoClient(mongo_uri)
db = client["study_bot"]
collection = db["chat_history"]

# Request Model
class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Get last 5 messages
        previous_chats = collection.find(
            {"user_id": request.user_id}
        ).sort("_id", -1).limit(5)

        context = ""
        for chat_item in previous_chats:
            context += f"User: {chat_item['user']}\nBot: {chat_item['bot']}\n"

        system_prompt = """
You are a helpful AI Study Assistant.
Answer only academic or learning-related questions clearly and simply.
If the question is not related to study, politely refuse.
"""

        full_prompt = system_prompt + "\n" + context + f"\nUser: {request.message}"

        # Invoke model
        response = llm.invoke(full_prompt)

        # Save to MongoDB
        collection.insert_one({
            "user_id": request.user_id,
            "user": request.message,
            "bot": response.content,
            "timestamp": datetime.utcnow()
        })

        return {"response": response.content}

    except Exception as e:
        print("🔥 ERROR:", e)
        return {"error": str(e)}

@app.get("/history/{user_id}")
def get_history(user_id: str):
    try:
        chats = list(collection.find({"user_id": user_id}, {"_id": 0}))
        return {"history": chats}
    except Exception as e:
        return {"error": str(e)}