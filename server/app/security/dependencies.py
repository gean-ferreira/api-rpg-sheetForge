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


# Função para verificar se o usuário pode acessar uma rota específica
async def get_user_if_allowed(
    user_id: int = Path(...), current_user_id: dict = Depends(get_current_user)
):
    # Verifica se o user_id do token é igual ao user_id passado na URL
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Você não tem permissão para acessar este recurso"
        )
