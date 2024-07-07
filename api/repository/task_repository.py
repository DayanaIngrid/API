from sqlalchemy.orm import Session
from datetime import datetime
from api.domain.model.models import Task

class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, description: str, status: str, created_at: datetime):
        task = Task(title=title, description=description, status=status, created_at=created_at)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def read(self, task_id: int):
        return self.session.query(Task).filter(Task.id == task_id).first()

    def update(self, task_id: int, title: str = None, description: str = None, status: str = None):
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if status is not None:
                task.status = status
            self.session.commit()
            self.session.refresh(task)
        return task

    def delete(self, task_id: int):
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            self.session.delete(task)
            self.session.commit()
        return task

    def find_all(self):
        return self.session.query(Task).all()
