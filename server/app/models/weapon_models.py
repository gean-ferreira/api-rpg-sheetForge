""" 
Este módulo define os modelos de dados para armas utilizadas no sistema de RPG
"""

from typing import List
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
    weapon_id: int
    name: str
    damage: str
    critical: str
    ability_modifier: str
    attack_range: str
    damage_type: str


#
# Respostas
#
class WeaponsListResponseModel(ResponseWithDataModel[List[WeaponBaseModel]]):
    pass
