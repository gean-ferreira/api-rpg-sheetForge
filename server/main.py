# Main file
from fastapi import FastAPI
from app.core.database import database
from app.api.user_routes import router as user_router

app = FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
