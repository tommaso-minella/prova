from datetime import datetime, timedelta, timezone
from typing import List, Optional
from bson.objectid import ObjectId
from .database import chat_collection, message_collection
from .schemas.chat import Chat as ChatSchema, ChatCreate as ChatCreateSchema
from .schemas.message import Message as MessageSchema, MessageCreate as MessageCreateSchema
import uuid
import logging

async def create_chat(user_id: str):
    chat = ChatCreateSchema(user_id=user_id, session_id=str(uuid.uuid4()))
    chat_dict = chat.dict()
    chat_dict["created_at"] = datetime.now(timezone.utc)
    chat_dict["updated_at"] = datetime.now(timezone.utc)
    result = await chat_collection.insert_one(chat_dict)
    new_chat = await chat_collection.find_one({"_id": result.inserted_id})
    new_chat = convert_objectid_to_str(new_chat)
    logging.info(f"New chat created with id: {new_chat['_id']}")
    return ChatSchema(**new_chat)

def convert_objectid_to_str(data: dict):
    if '_id' in data and isinstance(data['_id'], ObjectId):
        data['_id'] = str(data['_id'])
    return data

async def create_chat(user_id: str):
    chat = ChatCreateSchema(user_id=user_id, session_id=str(uuid.uuid4()))
    chat_dict = chat.dict()
    chat_dict["created_at"] = datetime.now(timezone.utc)
    chat_dict["updated_at"] = datetime.now(timezone.utc)
    result = await chat_collection.insert_one(chat_dict)
    new_chat = await chat_collection.find_one({"_id": result.inserted_id})
    new_chat = convert_objectid_to_str(new_chat)
    return ChatSchema(**new_chat)

async def get_chats(user_id: str, skip: int = 0, limit: int = 10) -> List[ChatSchema]:
    chats = await chat_collection.find({"user_id": user_id}).skip(skip).limit(limit).to_list(length=limit)
    return [ChatSchema(**convert_objectid_to_str(chat)) for chat in chats]

async def get_chat(user_id: str, chat_id: str) -> Optional[ChatSchema]:
    chat = await chat_collection.find_one({"user_id": user_id, "_id": ObjectId(chat_id)})
    if chat:
        chat = convert_objectid_to_str(chat)
        return ChatSchema(**chat)
    return None

async def delete_chat(user_id: str, chat_id: str) -> bool:
    result = await chat_collection.delete_one({"user_id": user_id, "_id": ObjectId(chat_id)})
    return result.deleted_count > 0

async def add_message_to_chat(user_id: str, chat_id: str, message: MessageSchema) -> Optional[ChatSchema]:
    message_dict = message.dict()
    if "timestamp" not in message_dict:
        message_dict["timestamp"] = datetime.now(timezone.utc)
    result = await chat_collection.update_one(
        {"user_id": user_id, "_id": ObjectId(chat_id)},
        {"$push": {"messages": message_dict}, "$set": {"updated_at": datetime.now(timezone.utc)}}
    )
    if result.modified_count > 0:
        return await get_chat(user_id, chat_id)
    return None

async def cleanup_sessions():
    expiration_time = datetime.now(timezone.utc) - timedelta(minutes=60)
    await chat_collection.delete_many({"updated_at": {"$lt": expiration_time}})

async def create_message(user_id: str, chat_id: str, message_data: dict):
    if "timestamp" not in message_data:
        message_data["timestamp"] = datetime.now(timezone.utc)
    user_message = MessageSchema(
        user_id=user_id,
        chat_id=chat_id,
        **message_data
    )
    chat = await add_message_to_chat(user_id, chat_id, user_message)
    if chat:
        #TODO RAG
        assistant_message = MessageSchema(
            role="assistant",
            content="<p>Hello! How can I assist you today?</p>",
            timestamp=datetime.now(timezone.utc)
        )
        chat = await add_message_to_chat(user_id, chat_id, assistant_message)
    return chat
