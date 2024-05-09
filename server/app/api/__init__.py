from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .weapon_routes import router as weapon_router

# Exporta lista com todos os roteadores
routers = [auth_router, user_router, weapon_router]
