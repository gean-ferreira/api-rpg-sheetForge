""" 
Este módulo define os modelos de dados utilizados para representar usuários no sistema
"""

from pydantic import BaseModel, EmailStr

class UserBaseModel(BaseModel):
    username: str
    email: EmailStr


class UserInModel(UserBaseModel):
    password: str


class UserOutModel(UserBaseModel):
    user_id: int


class UserUpdateModel(BaseModel):
    username: str


