import logging
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from api.domain.dto.dtos import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from api.domain.model.models import Task
from api.repository.task_repository import TaskRepository

class TaskService:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create(self, user_data: TaskCreateDTO) -> TaskDTO:
        logging.info('Criando uma novo tarefa.')
        user = Task(**user_data.model_dump())
        try:
            created = self.task_repository.save(user)
            return TypeAdapter(TaskDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar o tarefa: {user_data.model_dump()}')
            raise HTTPException(status_code=409, detail=f'Tarefa já existe na base: {e.args[0]}')

    def read(self, user_id: int) -> TaskDTO:
        logging.info('Buscando uma tarefa.')
        return TypeAdapter(TaskDTO).validate_python(self._read(user_id))

    def _read(self, user_id: int) -> Task:
        user = self.task_repository.read(user_id)
        if user is None:
            logging.error(f'Tarefa {user_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Tarefa {user_id} não encontrado.')
        return user

    def find_all(self) -> list[TaskDTO]:
        logging.info('Buscando todos as tarefas.')
        users = self.task_repository.find_all()
        return [TypeAdapter(TaskDTO).validate_python(user) for user in users]

    def update(self, user_id: int, user_data: TaskUpdateDTO):
        logging.info(f'Atualizando a tarefa {user_id}.')
        user = self._read(user_id)
        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        user_updated = self.task_repository.save(user)
        logging.info(f'Tarefa {user_id} atualizado: {user_updated}')
        return TypeAdapter(TaskDTO).validate_python(user_updated)

    def delete(self, user_id: int) -> int:
        user = self._read(user_id)
        self.task_repository.delete(user)
        logging.info(f'Tarefa {user_id} deletado')
        return user_id