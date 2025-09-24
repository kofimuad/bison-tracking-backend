from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BisonStats(BaseModel):
    total_frames: int
    total_detection: int
    max_bisons_in_frame: int
    avg_confidence: float
    fps: float
    timestamp: datetime = Field(default_factory=datetime.now())
    id: Optional[str] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: str}