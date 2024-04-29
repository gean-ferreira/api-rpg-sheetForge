from fastapi import APIRouter, status
from app.repositories.weapon_repository import WeaponRepository
from app.services.weapon_service import WeaponService
from app.models.weapon_models import WeaponBaseModel, WeaponsListResponseModel

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
