from pydantic import BaseModel
from typing import List, Optional


#
# Utilizado nos erros 404
#
class DetailErrorResponse(BaseModel):
    detail: str


class ErrorModel(BaseModel):
    message: str
    field: str


#
# Utilizado nos erros 422
#
class ErrorResponseModel(DetailErrorResponse, BaseModel):
    detail: str
    errors: Optional[List[ErrorModel]] = None
