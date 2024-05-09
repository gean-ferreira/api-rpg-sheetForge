import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "Error na leitura do SECRET_KEY para codificação JWT, verificar arquivo .env"
    )

ALGORITHM = "HS256"

