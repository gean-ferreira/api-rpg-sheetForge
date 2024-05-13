from fastapi import APIRouter, Depends, status
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel
from app.models.user_models import (
    UserInModel,
    UserOutDataModel,
    UserUpdateModel,
    UsersListResponseModel,
)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.security.dependencies import get_user_if_allowed

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
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        403: {
            "model": DetailErrorResponse,
            "description": "Caso o usuário não tem permissão para acessar esses dados, como tentar acessar informações de outro usuário.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que o usuário com o ID especificado não foi encontrado no sistema.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente, como um ID inválido.",
        },
    },
    summary="Busca Dados do Usuário",
    description="""
    Busca um usuário específico pela sua identificação única (ID).

    Esta operação requer que o usuário esteja autenticado e tenha permissão para acessar seus próprios dados. Retorna os dados do usuário, incluindo ID, nome de usuário e e-mail, caso encontrado. Em caso de erros de autenticação ou permissão, retorna 401 ou 403, respectivamente. Se o usuário não for encontrado, retorna um erro 404.
    """,
    tags=["Usuários"],
)
async def read_user_data(user_id: int, _=Depends(get_user_if_allowed)):
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


@router.put(
    "/users/{user_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Usuário atualizado com sucesso.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que o usuário já existe.",
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
    summary="Atualiza o nome de usuário",
    description="""
    Atualiza o username de um usuário existente na plataforma, identificado pelo seu ID único.

    É necessário fornecer um novo username que ainda não esteja em uso por outro usuário.
    """,
    tags=["Usuários"],
)
async def update_user_endpoint(user_id: int, req: UserUpdateModel):
    message = await user_service.update_user(user_id, req.username)
    return BaseResponseModel(message=message["message"])


@router.delete(
    "/users/{user_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Confirmação de que o usuário foi excluído com sucesso.",
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
    summary="Excluir Usuário",
    description="""
    Exclui um usuário específico da plataforma, identificado pelo seu ID único.
    
    Essa operação é irreversível. 
    Uma vez que um usuário é excluído, todos os dados associados a esse usuário serão permanentemente removidos. 
    Utilize essa operação com cuidado.
    """,
    tags=["Usuários"],
)
async def delete_user(user_id: int):
    message = await user_service.delete_user(user_id)
    return BaseResponseModel(message=message["message"])
