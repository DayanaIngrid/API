from datetime import datetime
from pydantic import BaseModel, ConfigDict
# field_validator
from typing import Optional

from api.domain.util.utils import Validate

class TaskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    # @field_validator('cpf')
    # def validate_cpf(cls, cpf):
    #     return Validate.cpf(cpf)

    # @field_validator('phone')
    # def validate_phone(cls, phone):
    #     return Validate.phone(phone)

class TaskCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    status: str

    # @field_validator('cpf')
    # def validate_cpf(cls, cpf):
    #     return Validate.cpf(cpf)

    # @field_validator('phone')
    # def validate_phone(cls, phone):
    #     return Validate.phone(phone)


class TaskUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    # @field_validator('phone')
    # def validate_phone(cls, phone):
    #     return Validate.phone(phone)


class TokenResponse(BaseModel):
    access_token: str
    expires_at: datetime


class UserTokenDataResponse(BaseModel):
    expires_at: datetime
