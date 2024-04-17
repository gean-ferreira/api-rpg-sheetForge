# Main file
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.database import database
from app.api.user_routes import router as user_router
from app.exceptions.exception_handlers import validation_exception_handler

app = FastAPI()
app.include_router(user_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
