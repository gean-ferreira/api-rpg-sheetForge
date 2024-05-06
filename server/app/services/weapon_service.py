""" 
Este módulo contém a lógica de serviço para operações relacionadas às armas no contexto do RPGs
"""

from fastapi import HTTPException, status
from app.repositories.weapon_repository import WeaponRepository
from app.models.weapon_models import WeaponBaseModel, WeaponOutModel


class WeaponService:
    def __init__(self, weapon_repository: WeaponRepository):
        self.weapon_repository = weapon_repository

    async def _verify_weapon_exists(self, weapon_id: int):
        db_weapon = await self.weapon_repository.get_weapon_by_id(weapon_id)
        if db_weapon is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Arma não encontrada"
            )
        return db_weapon

    async def get_weapons(self):
        weapons_records = await self.weapon_repository.get_weapons()
        weapons = [WeaponOutModel(**weapon) for weapon in weapons_records]
        return weapons

    async def get_weapon_by_id(self, weapon_id: int):
        db_weapon = await self._verify_weapon_exists(weapon_id)
        return WeaponOutModel(**db_weapon)

    async def create_weapon(self, weapon: WeaponBaseModel):
        db_weapon = await self.weapon_repository.create_weapon(weapon)
        weapon_data = WeaponOutModel(
            weapon_id=db_weapon,
            name=weapon.name,
            damage=weapon.damage,
            critical=weapon.critical,
            ability_modifier=weapon.ability_modifier,
            attack_range=weapon.attack_range,
            damage_type=weapon.damage_type,
        )
        return weapon_data
