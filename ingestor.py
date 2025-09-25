import requests
import json
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from database.connection import bison_db


load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

async def ingest_data():
    while True:
        try:
            response = requests.get("http://localhost:8080/stats") # This place is where the ingesting happens
            data = response.json()

            data["timestamp"] = datetime.now()

            await bison_db.detection_data.insert_one(data)

            print(f"Saved stats for frame: {data['total_frames']}")
        except requests.exceptions.ConnectionError:
            print("Waiting for inference server...")
        except Exception as e:
            print(f"An error occured: {e}")

        await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(ingest_data())