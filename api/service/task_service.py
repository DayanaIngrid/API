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
        logging.info('Criando uma nova tarefa.')
        try:
            created = self.task_repository.create(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                created_at=datetime.utcnow()  # Defina a data e hora de criação como o momento atual
            )
            return TypeAdapter(TaskDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar a tarefa: {task_data.dict()}')
            raise HTTPException(status_code=409, detail=f'Tarefa já existe na base: {e.args[0]}')

    def read(self, task_id: int) -> TaskDTO:
        logging.info('Buscando uma tarefa.')
        return TypeAdapter(TaskDTO).validate_python(self._read(task_id))

    def _read(self, task_id: int) -> Task:
        task = self.task_repository.read(task_id)
        if task is None:
            logging.error(f'Tarefa {task_id} não encontrada.')
            raise HTTPException(status_code=404, detail=f'Tarefa {task_id} não encontrada.')
        return task

    def find_all(self) -> list[TaskDTO]:
        logging.info('Buscando todas as tarefas.')
        tasks = self.task_repository.find_all()
        return [TypeAdapter(TaskDTO).validate_python(task) for task in tasks]

    def update(self, task_id: int, task_data: TaskUpdateDTO) -> TaskDTO:
        logging.info(f'Atualizando a tarefa {task_id}.')
        task = self._read(task_id)
        task_data_dict = task_data.dict(exclude_unset=True)
        for key, value in task_data_dict.items():
            setattr(task, key, value)
        task_updated = self.task_repository.save(task)
        logging.info(f'Tarefa {task_id} atualizada: {task_updated}')
        return TypeAdapter(TaskDTO).validate_python(task_updated)

    def delete(self, task_id: int) -> int:
        task = self._read(task_id)
        self.task_repository.delete(task_id)
        logging.info(f'Tarefa {task_id} deletada')
        return task_id
