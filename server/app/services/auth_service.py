""" 
Este módulo contém a lógica de serviço para operações relacionadas a autenticação
"""

from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.security.security import verify_password
from app.security.auth_handler import create_access_token


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def _authenticate_user(self, username: str, password: str):
        db_user = await self.user_repository.get_user_by_username(username)
        if db_user is None or not verify_password(password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário e/ou senha inválidos",
            )
        return db_user

    async def authenticate_and_generate_token(self, username: str, password: str):
        user = await self._authenticate_user(username, password)
        return create_access_token(user_id=user.user_id)