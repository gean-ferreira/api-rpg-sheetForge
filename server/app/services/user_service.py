""" 
Este módulo contém a lógica de serviço para operações relacionadas aos usuários
"""

from fastapi import HTTPException, status
from app.models.user_models import UserInModel, UserOutModel
from app.repositories.user_repository import UserRepository
from app.security.security import get_password_hash


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

    async def _verify_username_exists(self, username: str):
        db_user = await self.user_repository.get_user_by_username(username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já cadastrado",
            )
        return db_user

    async def _verify_email_exists(self, email: str):
        db_user = await self.user_repository.get_user_by_email(email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado",
            )
        return db_user

    async def get_users(self):
        users_records = await self.user_repository.get_users()
        users = [UserOutModel(**user) for user in users_records]
        return users

    async def get_user_by_id(self, user_id: int):
        db_user = await self._verify_user_exists(user_id)
        return UserOutModel(**db_user)

    async def create_user(self, user: UserInModel):
        user.password = await get_password_hash(user.password)
        await self._verify_username_exists(user.username)
        await self._verify_email_exists(user.email)
        db_user = await self.user_repository.create_user(user)
        user_data = UserOutModel(
            user_id=db_user, username=user.username, email=user.email
        )
        return user_data

    async def update_user(self, user_id: int, username: str):
        await self._verify_user_exists(user_id)
        await self._verify_username_exists(username)
        await self.user_repository.update_user(user_id, username)
        return {"message": "Username atualizado com sucesso"}

    async def delete_user(self, user_id: int):
        await self._verify_user_exists(user_id)
        await self.user_repository.delete_user(user_id)
        return {"message": "Usuário deletado com sucesso"}
