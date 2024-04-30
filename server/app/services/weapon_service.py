""" 
Este módulo contém a lógica de serviço para operações relacionadas às armas no contexto do RPGs
"""

from fastapi import HTTPException, status
from app.repositories.weapon_repository import WeaponRepository
from app.models.weapon_models import WeaponBaseModel


class WeaponService:
    def __init__(self, weapon_repository: WeaponRepository):
        self.weapon_repository = weapon_repository

    async def _verify_weapon_exists(self, weapon_id: int):
        db_weapon = await self.weapon_repository.get_weapon_by_id(weapon_id)
        return db_weapon

    async def get_weapons(self):
        weapons_records = await self.weapon_repository.get_weapons()
        weapons = [WeaponBaseModel(**weapon) for weapon in weapons_records]
        return weapons
