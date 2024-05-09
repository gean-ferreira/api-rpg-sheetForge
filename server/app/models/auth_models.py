from pydantic import BaseModel


class LoginFormData(BaseModel):
    username: str
    password: str
