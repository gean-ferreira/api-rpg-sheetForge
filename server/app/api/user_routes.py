from fastapi import APIRouter
from app.models.user_models import (
    UsersListResponseModel,
)

router = APIRouter()
user_service = UserService(UserRepository())


@router.get(
    "/users/",
    response_model=UsersListResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Lista Todos os Usuários",
    description="""
    Retorna uma lista de todos os usuários cadastrados na plataforma.
    
    Cada usuário é retornado com seu ID, nome de usuário e e-mail.
    Ideal para administradores monitorarem os usuários cadastrados.
    """,
    response_description="Uma lista de usuários, incluindo detalhes como ID, nome de usuário e e-mail.",
    tags=["Usuários"],
)
async def get_users():
    users = await user_service.get_users()
    return UsersListResponseModel(message="Usuários listados com sucesso", data=users)


