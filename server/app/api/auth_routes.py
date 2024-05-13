from datetime import datetime
from fastapi import APIRouter, Depends, Response
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.auth_models import LoginFormData
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import ResponseWithDataModel

router = APIRouter()
auth_service = AuthService(UserRepository())


@router.post(
    "/auth/login/",
    responses={
        200: {
            "model": ResponseWithDataModel,
            "description": "Login realizado com sucesso.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "Usuário e/ou senha inválidos.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados.",
        },
    },
    summary="Login do usuário",
    description="""
    Autentica um usuário na plataforma utilizando username e senha e retorna um token JWT se bem-sucedido.
    O token é retornado tanto no corpo da resposta quanto em um cookie HTTP-only.
    """,
    tags=["Auth"],
)
async def login(response: Response, form_data: LoginFormData = Depends()):
    access_token, expire = await auth_service.authenticate_and_generate_token(
        form_data.username, form_data.password
    )
    max_age = int((expire - datetime.utcnow()).total_seconds())
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
