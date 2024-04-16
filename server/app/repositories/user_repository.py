""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas aos usuários
"""

from app.core.database import database
from app.models.user_models import UserInModel


class UserRepository:
    async def get_users(self):
        query = "SELECT * FROM RPG.Users;"
        return await database.fetch_all(query)

    async def get_user_by_id(self, user_id: int):
        query = "SELECT * FROM RPG.Users WHERE user_id = :id;"
        return await database.fetch_one(query, {"id": user_id})

    async def create_user(self, user: UserInModel):
        query = "INSERT INTO RPG.Users (username, email, password_hash) VALUES (:username, :email, :hashed_password);"
        return await database.execute(
            query,
            {
                "username": user.username,
                "email": user.email,
                "hashed_password": user.password,
            },
        )

    async def update_user(self, user_id: int, username: str):
        query = "UPDATE RPG.Users SET username = :username WHERE user_id = :id;"
        return await database.execute(query, {"username": username, "id": user_id})

    async def delete_user(self, user_id: int):
        query = "DELETE FROM RPG.Users WHERE user_id = :id;"
        return await database.execute(query, {"id": user_id})
