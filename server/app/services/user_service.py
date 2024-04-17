""" 
Este módulo contém a lógica de serviço para operações relacionadas aos usuários
"""

from fastapi import HTTPException, status
from app.models.user_models import UserInModel, UserOutModel
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def _verify_user_exists(self, user_id: int):
        db_user = await self.user_repository.get_user_by_id(user_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )
        return db_user


    async def get_users(self):
        users_records = await self.user_repository.get_users()
        users = [UserOutModel(**user) for user in users_records]
        return users

    async def get_user_by_id(self, user_id: int):
        db_user = await self._verify_user_exists(user_id)
        return UserOutModel(**db_user)

