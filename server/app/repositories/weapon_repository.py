""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas às armas no contexto do RPG
"""

from app.core.database import database


class WeaponRepository:
    async def get_weapons(self):
        query = "SELECT * FROM RPG.Weapons;"
        return await database.fetch_all(query)

    async def get_weapon_by_id(self, weapon_id: int):
        query = "SELECT * FROM RPG.Weapons WHERE weapon_id = :id;"
        return await database.fetch_one(query, {"id": weapon_id})
