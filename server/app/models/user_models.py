""" 
Este módulo define os modelos de dados utilizados para representar usuários no sistema
"""

from pydantic import BaseModel, EmailStr
from typing import List

from app.models.response_models import ResponseWithDataModel


class UserBaseModel(BaseModel):
    username: str
    email: EmailStr


class UserInModel(UserBaseModel):
    password: str


class UserOutModel(UserBaseModel):
    user_id: int


class UserUpdateModel(BaseModel):
    username: str


#
# Respostas
#
class UsersListResponseModel(ResponseWithDataModel[List[UserOutModel]]):
    pass


class UserOutDataModel(ResponseWithDataModel[UserOutModel]):
    pass
