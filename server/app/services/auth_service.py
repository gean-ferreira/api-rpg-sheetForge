""" 
Este módulo contém a lógica de serviço para operações relacionadas a autenticação
"""

from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.security.security import verify_password

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
