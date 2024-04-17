from fastapi import APIRouter
from fastapi import APIRouter, status
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.user_models import (
    UserOutDataModel,
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


@router.get(
    "/users/{user_id}/",
    responses={
        200: {
            "model": UserOutDataModel,
            "description": "Os detalhes do usuário, incluindo ID, nome de usuário e e-mail, são retornados na resposta.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que o usuário não foi encontrado.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados.",
        },
    },
    summary="Busca Dados do Usuário",
    description="""
    Busca um usuário específico pela sua identificação única (ID).

    Retorna os dados do usuário, incluindo ID, nome de usuário e e-mail, caso encontrado.
    Caso contrário, retorna um erro 404 indicando que o usuário não foi encontrado.
    """,
    tags=["Usuários"],
)
async def read_user_data(user_id: int):
    db_user = await user_service.get_user_by_id(user_id)
    return UserOutDataModel(
        message="Dados do usuário encontrados com sucesso", data=db_user
    )


