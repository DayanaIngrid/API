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

    def create(self, task_data: TaskCreateDTO) -> TaskDTO:
        logging.info('Criando uma novo tarefa.')
        task = Task(**task_data.model_dump())
        try:
            created = self.task_repository.save(Task)
            return TypeAdapter(TaskDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar o tarefa: {task_data.model_dump()}')
            raise HTTPException(status_code=409, detail=f'Tarefa já existe na base: {e.args[0]}')

    def read(self, task_id: int) -> TaskDTO:
        logging.info('Buscando uma tarefa.')
        return TypeAdapter(TaskDTO).validate_python(self._read(task_id))

    def _read(self, task_id: int) -> Task:
        task = self.task_repository.read(task_id)
        if task is None:
            logging.error(f'Tarefa {task_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Tarefa {task_id} não encontrado.')
        return task

    def find_all(self) -> list[TaskDTO]:
        logging.info('Buscando todos as tarefas.')
        tasks = self.task_repository.find_all()
        return [TypeAdapter(TaskDTO).validate_python(task) for task in tasks]

    def update(self, task_id: int, task_data: TaskUpdateDTO):
        logging.info(f'Atualizando a tarefa {task_id}.')
        task = self._read(task_id)
        task_data = task_data.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(task, key, value)
        task_updated = self.task_repository.save(task)
        logging.info(f'Tarefa {task_id} atualizado: {task_updated}')
        return TypeAdapter(TaskDTO).validate_python(task_updated)

    def delete(self, task_id: int) -> int:
        task = self._read(task_id)
        self.task_repository.delete(task)
        logging.info(f'Tarefa {task_id} deletado')
        return task_id