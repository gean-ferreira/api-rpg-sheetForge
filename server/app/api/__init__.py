from .user_routes import router as user_router
from .weapon_routes import router as weapon_router

# Exporta lista com todos os roteadores
routers = [user_router, weapon_router]
