from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

from api.domain.util.utils import Validate
# não faz sentido em um api de gerenciamento de tarefas, mas pode ser usado para outro exemplo, apenas descomentar essa parte. 



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

    # Faz parte do validador, descomentar caso queira usar.


class TaskCreateDTO(BaseModel):
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
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]

    # @field_validator('phone')
    # def validate_phone(cls, phone):
    #     return Validate.phone(phone)


class TokenResponse(BaseModel):
    access_token: str
    expires_at: datetime


class UserTokenDataResponse(BaseModel):
    expires_at: datetime
