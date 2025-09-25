import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

bison_db = client["bison_tracking_db"]

detection_data = bison_db["Detection Data"]