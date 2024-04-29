""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas às armas no contexto do RPG
"""

from app.core.database import database


class WeaponRepository:
    async def get_weapons(self):
        query = "SELECT * FROM RPG.Weapons;"
        return await database.fetch_all(query)
