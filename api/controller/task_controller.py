from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.config.auth_config import get_current_user
from api.config.database import get_db
from api.domain.dto.dtos import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from api.repository.task_repository import TaskRepository
from api.service.task_service import TaskService

user_router = APIRouter(prefix='/users', tags=['Users'])


def get_user_repo(session: Session = Depends(get_db)):
    return TaskRepository(session=session)


@user_router.post('/', status_code=201, description='cria um novo usuário', response_model=TaskDTO)
async def create(
        request: TaskCreateDTO,
        user_repo: TaskRepository = Depends(get_user_repo),
        authorization: str = Depends(get_current_user)
):
    usuario_service = TaskRepository(user_repo)
    return usuario_service.create(request)


@user_router.get('/{user_id}', status_code=200, description='Buscar usuario por ID', response_model=TaskDTO)
async def find_by_id(user_id: int, user_repo: TaskRepository = Depends(get_user_repo),
                     authorization: str = Depends(get_current_user)):
    usuario_service = TaskService(user_repo)
    return usuario_service.read(user_id=user_id)


@user_router.get('/', status_code=200, description='Buscar todos os usuários', response_model=list[TaskDTO])
async def find_all(user_repo: TaskRepository = Depends(get_user_repo),
                   authorization: str = Depends(get_current_user)):
    usuario_service = TaskService(user_repo)
    return usuario_service.find_all()


@user_router.put('/{user_id}', status_code=200, description='Atualizar um usuário', response_model=TaskDTO)
async def find_all(user_id: int, user_data: TaskUpdateDTO, user_repo: TaskRepository = Depends(get_user_repo),
                   authorization: str = Depends(get_current_user)):
    usuario_service = TaskService(user_repo)
    return usuario_service.update(user_id, user_data)


@user_router.delete('/{user_id}', status_code=204, description='Deletar usuario por ID')
async def find_by_id(user_id: int, user_repo: TaskRepository = Depends(get_user_repo),
                     authorization: str = Depends(get_current_user)):
    usuario_service = TaskService(user_repo)
    usuario_service.delete(user_id=user_id)
