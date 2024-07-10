from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.config.auth_config import get_current_user
from api.config.database import get_db
from api.domain.dto.dtos import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from api.repository.task_repository import TaskRepository
from api.service.task_service import TaskService

user_router = APIRouter(prefix='/tasks', tags=['Tasks'])


def get_task_repo(session: Session = Depends(get_db)):
    return TaskRepository(session=session)


@task_router.post('/', status_code=201, description='Cria uma nova tarefa', response_model=TaskDTO)
async def create_task(
        request: TaskCreateDTO,
        task_repo: TaskRepository = Depends(get_task_repo),
        authorization: str = Depends(get_current_user)
):
    task_service = TaskService(task_repo)
    return task_service.create(title=request.title, description=request.description, status=request.status, created_at=request.created_at)


@task_router.get('/{task_id}', status_code=200, description='Buscar tarefa por ID', response_model=TaskDTO)
async def find_task_by_id(task_id: int, task_repo: TaskRepository = Depends(get_task_repo),
                          authorization: str = Depends(get_current_user)):
    task_service = TaskService(task_repo)
    return task_service.read(task_id=task_id)


@task_router.get('/', status_code=200, description='Buscar todas as tarefas', response_model=list[TaskDTO])
async def find_all_tasks(task_repo: TaskRepository = Depends(get_task_repo),
                         authorization: str = Depends(get_current_user)):
    task_service = TaskService(task_repo)
    return task_service.find_all()


@task_router.put('/{task_id}', status_code=200, description='Atualizar uma tarefa', response_model=TaskDTO)
async def update_task(task_id: int, task_data: TaskUpdateDTO, task_repo: TaskRepository = Depends(get_task_repo),
                      authorization: str = Depends(get_current_user)):
    task_service = TaskService(task_repo)
    return task_service.update(task_id, title=task_data.title, description=task_data.description, status=task_data.status)


@task_router.delete('/{task_id}', status_code=204, description='Deletar tarefa por ID')
async def delete_task(task_id: int, task_repo: TaskRepository = Depends(get_task_repo),
                      authorization: str = Depends(get_current_user)):
    task_service = TaskService(task_repo)
    task_service.delete(task_id=task_id)