from fastapi import APIRouter, status
from app.repositories.weapon_repository import WeaponRepository
from app.services.weapon_service import WeaponService
from app.models.weapon_models import WeaponOutDataModel, WeaponsListResponseModel
from app.models.error_models import DetailErrorResponse, ErrorResponseModel

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
