from sqlalchemy import Column, Integer, String, DateTime
from api.config.database import Base, engine

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    status = Column(String(20), nullable=False)  # Pode ser "Pendente", "Em Progresso", "Concluída"
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Task(id={self.id}, title={self.title}, status={self.status})>'

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
