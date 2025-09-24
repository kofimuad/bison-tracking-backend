from fastapi import APIRouter, HTTPException, status
from typing import List
from database.connection import bison_db
from models.bison_model import BisonStats


bison_router = APIRouter()

@bison_router.get("/latest_stats", response_model=BisonStats, status_code=status.HTTP_200_OK, response_description="Get the latest bison tracking stats")
async def get_latest_stats():
    latest_stats = await bison_db.detection_data.find_one({}, sort=[("timestamp", -1)])

    if latest_stats:
        return latest_stats
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No detection data found")