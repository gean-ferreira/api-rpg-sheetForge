from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel


DataType = TypeVar("DataType")


class BaseResponseModel(BaseModel):
    message: str


class ResponseWithDataModel(BaseResponseModel, GenericModel, Generic[DataType]):
    data: DataType
