from fastapi import FastAPI, HTTPException, Header
from typing import List
from bson.objectid import ObjectId
from src.schemas.chat import Chat as ChatSchema, ChatCreate as ChatCreateSchema
from src.schemas.message import MessageCreate as MessageCreateSchema
from src.crud import create_chat, get_chats, get_chat, delete_chat, create_message, cleanup_sessions
import asyncio
import os
import logging


# Debug line to check environment variable
print("MONGODB_CONNECTION_STRING:", os.getenv("MONGODB_CONNECTION_STRING"))

app = FastAPI()

@app.post("/chats/", response_model=ChatSchema)
async def create_chat_endpoint(user_id: str = Header(...)):
    return await create_chat(user_id=user_id)

@app.get("/chats/", response_model=List[ChatSchema])
async def read_chats(user_id: str = Header(...), skip: int = 0, limit: int = 10):
    return await get_chats(user_id=user_id, skip=skip, limit=limit)

@app.get("/chats/{chat_id}", response_model=ChatSchema)
async def read_chat(chat_id: str, user_id: str = Header(...)):
    chat = await get_chat(user_id=user_id, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@app.post("/chats/{chat_id}/messages/", response_model=ChatSchema)
async def add_message_endpoint(chat_id: str, message: MessageCreateSchema, user_id: str = Header(...)):
    logging.info(f"Adding message to chat_id: {chat_id}")
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=400, detail="Invalid chat_id format")
    updated_chat = await create_message(user_id=user_id, chat_id=chat_id, message_data=message.dict())
    if updated_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return updated_chat

@app.delete("/chats/{chat_id}")
async def delete_chat_endpoint(chat_id: str, user_id: str = Header(...)):
    logging.info(f"Deleting chat_id: {chat_id}")
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=400, detail="Invalid chat_id format")
    success = await delete_chat(user_id=user_id, chat_id=chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted"}

async def cleanup_sessions_periodically():
    while True:
        await cleanup_sessions()
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_sessions_periodically())
