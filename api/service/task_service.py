import logging
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from api.domain.dto.dtos import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from api.domain.model.models import Task
from api.repository.task_repository import TaskRepository

class TaskService:

    def __init__(self, task_repository: TaskRepository):
        self.usuario_repository = task_repository

    def create(self, user_data: TaskCreateDTO) -> UsuarioDTO:
        logging.info('Criando um novo usuario.')
        user = Usuario(**user_data.model_dump())
        try:
            created = self.usuario_repository.save(user)
            return TypeAdapter(UsuarioDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar o usuário: {user_data.model_dump()}')
            raise HTTPException(status_code=409, detail=f'Usuario já existe na base: {e.args[0]}')

    def read(self, user_id: int) -> UsuarioDTO:
        logging.info('Buscando um usuario.')
        return TypeAdapter(UsuarioDTO).validate_python(self._read(user_id))

    def _read(self, user_id: int) -> Usuario:
        user = self.usuario_repository.read(user_id)
        if user is None:
            logging.error(f'Usuário {user_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Usuário {user_id} não encontrado.')
        return user

    def find_all(self) -> list[UsuarioDTO]:
        logging.info('Buscando todos os usuários.')
        users = self.usuario_repository.find_all()
        return [TypeAdapter(UsuarioDTO).validate_python(user) for user in users]

    def update(self, user_id: int, user_data: UsuarioUpdateDTO):
        logging.info(f'Atualizando o usuario {user_id}.')
        user = self._read(user_id)
        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        user_updated = self.usuario_repository.save(user)
        logging.info(f'Usuario {user_id} atualizado: {user_updated}')
        return TypeAdapter(UsuarioDTO).validate_python(user_updated)

    def delete(self, user_id: int) -> int:
        user = self._read(user_id)
        self.usuario_repository.delete(user)
        logging.info(f'Usuario {user_id} deletado')
        return user_id