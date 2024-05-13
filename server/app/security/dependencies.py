from fastapi import Depends, HTTPException, Path, status
from fastapi.security import APIKeyHeader
from .auth_handler import decode_access_token

# Configuração simplificada para apenas incluir o token na modal do Swagger
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


# Função para obter o usuário atual baseado no token
def get_current_user(token: str = Depends(api_key_header)):
    payload = decode_access_token(token)
    return int(payload["sub"])


# Função para verificar se o usuário pode acessar uma rota específica
async def get_user_if_allowed(
    user_id: int = Path(...), current_user_id: int = Depends(get_current_user)
):
    # Verifica se o user_id do token é igual ao user_id passado na URL
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Você não tem permissão para acessar este recurso"
        )
