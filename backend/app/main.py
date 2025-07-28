from fastapi import FastAPI
from backend.app.db.connect import AsyncDBPool
from backend.app.api.auth import router as auth_router
from backend.app.api.users import router as user_router
from backend.app.api.parking import router as parking_lot_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await AsyncDBPool.init_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await AsyncDBPool.close_pool()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(parking_lot_router)