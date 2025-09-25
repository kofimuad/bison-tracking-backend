from fastapi import APIRouter, HTTPException, status
from typing import List
from database.connection import bison_db
from models.bison_model import BisonStats
# from pymongo import DESCENDING
from utils import replace_mongo_id
bison_router = APIRouter()

@bison_router.get("/latest_stats", response_model=BisonStats, status_code=status.HTTP_200_OK, response_description="Get the latest bison tracking stats")
async def get_latest_stats():
    latest_stats = await bison_db.dectection_data.find_one(
        {}, sort=[("timestamp", -1)]
    )
    if not latest_stats:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No detection data found"
    )
    latest_stats["_id"] = str(latest_stats["_id"])
    return BisonStats(**latest_stats)