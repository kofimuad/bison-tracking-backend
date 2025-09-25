from fastapi import APIRouter, HTTPException, status
from typing import List
from database.connection import bison_db
from models.bison_model import BisonStats
from typing import List
from bson.objectid import ObjectId
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

@bison_router.get("/all_stats", response_model=List[BisonStats], status_code=status.HTTP_200_OK, response_description="Get all bison tracking stats")
async def get_all_stats():
    all_stats = bison_db.dectection_data.find({})
    all_stats_list = await all_stats.to_list(length=1000000)
    if not all_stats_list:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No detection data found"
    )
    return [
        BisonStats(**{
            **stat, 
            "_id": str(stat["_id"]) # Convert ObjectId to string for Pydantic
        }) 
        for stat in all_stats_list
    ]