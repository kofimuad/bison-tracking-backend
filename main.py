from fastapi import FastAPI
from routers.stats_router import bison_router

app = FastAPI(title="Real Time Bison Tracking System API", version="1.0.0")

app.include_router(bison_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)