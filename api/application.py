from api.config.database import get_db
from api.domain.dto.dtos import TaskCreateDTO, TaskUpdateDTO
from api.repository.task_repository import TaskRepository
from api.service.task_service import TaskService


def main():
    with get_db() as session:
        task_repository = TaskRepository(session=session)
        task_service = TaskService(task_repository)

        # CREATE
        task_create_dto = TaskCreateDTO(
            title="Nome",
            description="Descrição",
            status="Status",
        )
        task_to_created = task_service.create(task_create_dto)
        task_id = task_to_created.id
        print(f'task created with id: {task_id}')

        # READ
        task_read = task_service.read(task_id=task_id)
        print(f'task read: {task_read}')

        # UPDATE
        task_update_data = TaskUpdateDTO(
            title="Nome",
            description="Descrição",
            status="Status",
        )
        task_updated = task_service.update(task_id=task_id, task_data=task_update_data)
        print(f'task updated: {task_updated}')

        # DELETE
        task_deleted_id = task_service.delete(task_id)
        print(f'task deleted with id: {task_deleted_id}')


if __name__ == '__main__':
    main()