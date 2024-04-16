from fastapi import APIRouter
from app.models.user_models import (
    UsersListResponseModel,
)

router = APIRouter()
user_service = UserService(UserRepository())


@router.get(
    "/users/"
)
async def get_users():
    users = await user_service.get_users()
    return UsersListResponseModel(message="Usuários listados com sucesso", data=users)


