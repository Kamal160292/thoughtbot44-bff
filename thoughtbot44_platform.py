from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import openai
import os

app = FastAPI()

# Load OpenAI API Key Securely from Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

BACKEND_URL = "https://tara-ai-backend.onrender.com"

# Thought Bot 44 - AI Request Model
class ThoughtBotRequest(BaseModel):
    user_id: str
    query_type: str
    user_input: str
    conversation_history: list = []  # Stores past messages for AI context

# AI Memory & Context Tracking
conversation_state = {}

# AUM 1.9413 Decisioning Engine (Universal Thought Processing)
def aum_decisioning_engine(user_id, query_type, user_input):
    if user_id not in conversation_state:
        conversation_state[user_id] = []

    conversation_state[user_id].append({"role": "user", "text": user_input})

    # 🔹 Intelligent Decisioning: Should GPT-4o Handle This or an API?
    if "quote" in user_input.lower():
        response_text = "I can generate a quote for you. What coverage amount are you looking for?"
        return {
            "decision": "collect_info",
            "message": response_text,
            "conversation_history": conversation_state[user_id]
        }

    elif "recommend" in user_input.lower():
        response_text = "Tell me your budget range, and I'll suggest the best policies."
        return {
            "decision": "collect_info",
            "message": response_text,
            "conversation_history": conversation_state[user_id]
        }

    elif "roleplay" in user_input.lower():
        response_text = "Let's start a sales roleplay! I'll be the customer."
        return {
            "decision": "ai_roleplay",
            "message": response_text,
            "conversation_history": conversation_state[user_id]
        }

    # If no specific decision, send it to GPT-4o for AI Response
    messages = [{"role": "system", "content": "You are Thought Bot 44, an AI-driven assistant running on AUM 1.9413."}]
    
    for message in conversation_state[user_id]:
        messages.append({"role": message["role"], "content": message["text"]})

    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    ai_response = response["choices"][0]["message"]["content"]
    
    conversation_state[user_id].append({"role": "bot", "text": ai_response})

    return {
        "decision": "ai_response",
        "message": ai_response,
        "conversation_history": conversation_state[user_id]
    }

@app.post("/thoughtbot44")
def process_chat(request: ThoughtBotRequest):
    return aum_decisioning_engine(request.user_id, request.query_type, request.user_input)

