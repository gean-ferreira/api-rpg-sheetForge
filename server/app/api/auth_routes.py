from fastapi import APIRouter, Depends
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.auth_models import LoginFormData

router = APIRouter()
auth_service = AuthService(UserRepository())


@router.post("/auth/login/")
async def login(form_data: LoginFormData = Depends()):
    access_token, expire = await auth_service.authenticate_and_generate_token(
        form_data.username, form_data.password
    )
    return ResponseWithDataModel(
        message="Login efetuado com sucesso",
        data={"access_token": access_token, "token_type": "bearer"},
    )
