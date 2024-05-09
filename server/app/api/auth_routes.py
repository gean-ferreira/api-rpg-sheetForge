from datetime import datetime
from fastapi import APIRouter, Depends, Response
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.auth_models import LoginFormData

router = APIRouter()
auth_service = AuthService(UserRepository())


async def login(response: Response, form_data: LoginFormData = Depends()):
    access_token, expire = await auth_service.authenticate_and_generate_token(
        form_data.username, form_data.password
    )
    max_age = int((expire - datetime.now()).total_seconds())
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=max_age,
        secure=True,
        samesite="Strict",
    )
    return ResponseWithDataModel(
        message="Login efetuado com sucesso",
        data={"access_token": access_token, "token_type": "bearer"},
    )
