from fastapi import APIRouter, status
from app.repositories.weapon_repository import WeaponRepository
from app.services.weapon_service import WeaponService
from app.models.weapon_models import (
    WeaponBaseModel,
    WeaponOutDataModel,
    WeaponsListResponseModel,
)
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel

router = APIRouter()
weapon_service = WeaponService(WeaponRepository())


@router.get(
    "/weapons/",
    response_model=WeaponsListResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Lista Todas as Armas",
    description="""
    Retorna uma lista de todas as armas disponíveis na plataforma.
    
    Cada arma é retornada com detalhes como ID, nome, dano, crítico, modificador de habilidade, alcance e tipo.
    Ideal para jogadores e mestres visualizarem as opções de armamento disponíveis.
    """,
    response_description="Uma lista de armas, incluindo detalhes como ID, nome, dano, crítico, modificador de habilidade, alcance e tipo.",
    tags=["Armas"],
)
async def get_weapons():
    weapons = await weapon_service.get_weapons()
    return WeaponsListResponseModel(message="Armas listados com sucesso", data=weapons)


@router.get(
    "/weapons/{weapon_id}/",
    responses={
        200: {
            "model": WeaponOutDataModel,
            "description": "Retorna os detalhes completos da arma, incluindo ID, nome, tipo de dano, e mais.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a arma não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados.",
        },
    },
    summary="Busca Dados da Arma",
    description="""
    Busca uma arma específica pelo seu ID.

    Retorna os detalhes completos da arma, incluindo ID, nome, tipo de dano, e outros atributos relevantes.
    Se a arma não for encontrada, retorna um erro 404.
    """,
    tags=["Armas"],
)
async def read_weapon_data(weapon_id: int):
    db_weapon = await weapon_service.get_weapon_by_id(weapon_id)
    return WeaponOutDataModel(
        message="Dados da arma encontrados com sucesso", data=db_weapon
    )


@router.post(
    "/weapons/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": WeaponOutDataModel,
            "description": "Arma criada com sucesso. Retorna os detalhes da nova arma.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Falha na criação da arma devido à tentativa de uso de um nome já existente.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente, como um tipo de dano inválido.",
        },
    },
    summary="Cria uma Nova Arma",
    description="""
    Registra uma nova arma no sistema.

    Para criar uma arma, é necessário fornecer detalhes como nome, tipo de dano, alcance de ataque (opcional), entre outros atributos relevantes.

    Em caso de sucesso, retorna os detalhes da arma criada. Se houver dados duplicados, como de um nome já utilizado, um erro será retornado.
    """,
    tags=["Armas"],
)
async def create_weapon(weapon: WeaponBaseModel):
    db_weapon = await weapon_service.create_weapon(weapon)
    return WeaponOutDataModel(message="Arma cadastrada com sucesso", data=db_weapon)


@router.put(
    "/weapons/{weapon_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Arma atualizada com sucesso. Retorna a confirmação da atualização.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Falha na atualização devido a dados duplicados, como um nome de arma já existente.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a arma não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente ou faltantes.",
        },
    },
    summary="Atualiza os dados de uma arma",
    description="""
    Atualiza detalhes de uma arma existente no sistema, identificada pelo seu ID único.

    É necessário fornecer os novos dados da arma que deseja atualizar. Se a arma não for encontrada, um erro será retornado.
    """,
    tags=["Armas"],
)
async def update_weapon(weapon_id: int, req: WeaponBaseModel):
    message = await weapon_service.update_weapon(weapon_id, req)
    return BaseResponseModel(message=message["message"])


@router.delete(
    "/weapons/{user_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Confirmação de que a arma foi excluída com sucesso.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a arma não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por tentativas de deletar uma arma com um ID inválido.",
        },
    },
    summary="Excluir Arma",
    description="""
    Exclui uma arma específica do sistema, identificada pelo seu ID único.
    
    Essa operação é irreversível. 
    Uma vez que uma arma é excluída, todos os dados associados a essa arma serão permanentemente removidos. 
    Utilize essa operação com cuidado.
    """,
    tags=["Armas"],
)
async def delete_user(weapon_id: int):
    message = await weapon_service.delete_weapon(weapon_id)
    return BaseResponseModel(message=message["message"])
