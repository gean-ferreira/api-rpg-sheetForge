""" 
Este módulo contém a lógica de serviço para operações relacionadas às armas no contexto do RPGs
"""

from app.repositories.weapon_repository import WeaponRepository
from app.models.weapon_models import WeaponBaseModel


class WeaponService:
    def __init__(self, weapon_repository: WeaponRepository):
        self.weapon_repository = weapon_repository

    async def get_weapons(self):
        weapons_records = await self.weapon_repository.get_weapons()
        weapons = [WeaponBaseModel(**weapon) for weapon in weapons_records]
        return weapons
