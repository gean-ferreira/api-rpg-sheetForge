""" 
Este módulo define os modelos de dados para armas utilizadas no sistema de RPG
"""

from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

from app.models.response_models import ResponseWithDataModel


class AbilityModifier(Enum):
    FORÇA = "For"
    DESTREZA = "Des"
    INTELIGÊNCIA = "Int"


class WeaponType(Enum):
    ESMAGAMENTO = "Esmagamento"
    PERFURAÇÃO = "Perfuração"
    CORTE = "Corte"


class WeaponBaseModel(BaseModel):
    name: str
    damage: str
    critical: str
    ability_modifier: AbilityModifier
    attack_range: Optional[str] = None
    damage_type: WeaponType


class WeaponOutModel(WeaponBaseModel):
    weapon_id: int


#
# Respostas
#
class WeaponsListResponseModel(ResponseWithDataModel[List[WeaponOutModel]]):
    pass


class WeaponOutDataModel(ResponseWithDataModel[WeaponOutModel]):
    pass
