""" 
Este módulo contém a lógica de serviço para operações relacionadas às armas no contexto do RPGs
"""

from app.repositories.weapon_repository import WeaponRepository


class WeaponService:
    def __init__(self, weapon_repository: WeaponRepository):
        self.weapon_repository = weapon_repository
