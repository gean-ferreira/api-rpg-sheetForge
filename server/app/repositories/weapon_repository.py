""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas às armas no contexto do RPG
"""

from app.core.database import database
from app.models.weapon_models import WeaponBaseModel


class WeaponRepository:
    async def get_weapons(self):
        query = "SELECT * FROM RPG.Weapons;"
        return await database.fetch_all(query)

    async def get_weapon_by_id(self, weapon_id: int):
        query = "SELECT * FROM RPG.Weapons WHERE weapon_id = :id;"
        return await database.fetch_one(query, {"id": weapon_id})

    async def get_weapon_by_name(self, name: str):
        query = "SELECT * FROM RPG.Weapons WHERE name = :name"
        return await database.fetch_one(query, {"name": name})

    async def create_weapon(self, weapon: WeaponBaseModel):
        query = """
        INSERT INTO RPG.Weapons (name, damage, critical, ability_modifier, attack_range, damage_type) 
        VALUES (:name, :damage, :critical, :ability_modifier, :attack_range, :damage_type);
        """
        return await database.execute(
            query,
            {
                "name": weapon.name,
                "damage": weapon.damage,
                "critical": weapon.critical,
                "ability_modifier": weapon.ability_modifier.value,
                "attack_range": weapon.attack_range,
                "damage_type": weapon.damage_type.value,
            },
        )

    async def update_weapon(self, weapon_id: int, weapon: WeaponBaseModel):
        query = """
        UPDATE RPG.Weapons 
        SET name = :name, 
            damage = :damage, 
            critical = :critical, 
            ability_modifier = :ability_modifier, 
            attack_range = :attack_range, 
            damage_type = :damage_type 
        WHERE weapon_id = :id;
        """
        return await database.execute(
            query,
            {
                "id": weapon_id,
                "name": weapon.name,
                "damage": weapon.damage,
                "critical": weapon.critical,
                "ability_modifier": weapon.ability_modifier.value,
                "attack_range": weapon.attack_range,
                "damage_type": weapon.damage_type.value,
            },
        )

    async def delete_weapon(self, weapon_id: int):
        query = "DELETE FROM RPG.Weapons WHERE weapon_id = :id;"
        return await database.execute(query, {"id": weapon_id})
