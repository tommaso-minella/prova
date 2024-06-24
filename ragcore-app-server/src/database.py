from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client.ragcore

chat_collection = database.get_collection("chats")
message_collection = database.get_collection("messages")
