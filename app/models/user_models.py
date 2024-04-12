""" 
Este módulo define os modelos de dados utilizados para representar usuários no sistema
"""

from pydantic import BaseModel, EmailStr

class UserBaseModel(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: str
