from fastapi import APIRouter
from fastapi import APIRouter, status
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel
from app.models.user_models import (
    UserInModel,
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


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": UserOutDataModel,
            "description": "Usuário criado com sucesso. Retorna os detalhes do novo usuário, exceto a senha.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Falha na criação do usuário devido à tentativa de uso de um e-mail ou username já existente.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente, como um e-mail inválido.",
        },
    },
    summary="Cria um Novo Usuário",
    description="""
    Registra um novo usuário na plataforma. 

    Para criar um usuário, é necessário fornecer um nome de usuário, um endereço de e-mail e uma senha. A senha fornecida será criptografada antes de ser armazenada.

    Em caso de sucesso, retorna os dados do usuário criado. Se o nome de usuário ou e-mail já estiverem em uso, um erro será retornado.
    """,
    tags=["Usuários"],
)
async def create_user(user: UserInModel):
    db_user = await user_service.create_user(user)
    return UserOutDataModel(message="Usuário cadastrado com sucesso", data=db_user)


