""" 
Este módulo contém a lógica de serviço para operações relacionadas aos usuários
"""
from app.models.user_models import UserOutModel
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    async def get_users(self):
        users_records = await self.user_repository.get_users()
        users = [UserOutModel(**user) for user in users_records]
        return users

