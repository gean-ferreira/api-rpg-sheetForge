from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from .auth_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Função para obter o usuário atual baseado no token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")  # Supondo que o sub seja uma string
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)
