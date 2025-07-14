from fastapi import FastAPI
from backend.app.db.async_connect import AsyncDBPool
from backend.app.api.auth import router as auth_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await AsyncDBPool.init_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await AsyncDBPool.close_pool()

app.include_router(auth_router)