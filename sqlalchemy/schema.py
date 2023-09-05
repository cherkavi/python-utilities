from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from . import JobStatus

Base = declarative_base()
#  The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)

class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True, nullable=False)
    number_of_chunks = Column(Integer, nullable=False)
    job_config = Column(JSON, nullable=True)

    chunks = relationship("JobChunk", back_populates="job")


class JobChunk(Base):
    __tablename__ = "job_chunk"
    id = Column(Integer, primary_key=True)
    chunk_id = Column(String, unique=True, nullable=False)
    job_id = Column(String, ForeignKey("job.job_id"))
    job = relationship("Job", back_populates="chunks")

    tasks = relationship("Task", back_populates="job_chunk")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String(50))
    information = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    job_chunk_id = Column(String, ForeignKey("job_chunk.chunk_id"))
    job_chunk = relationship("JobChunk", back_populates="tasks")

    status = relationship("TaskStatus", uselist=False, back_populates="task")

    __mapper_args__ = {"polymorphic_identity": "task", "polymorphic_on": type}

    def __repr__(self):
        return f"Task: {self.name}, {self.information}"


class SimulationTask(Task):
    __tablename__ = "simulation_task"

    id = Column(ForeignKey("task.id"), primary_key=True)
    simulation_id = Column(String, unique=True, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "simulation_task"}


class TaskStatus(Base):
    __tablename__ = "task_status"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(JobStatus), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    task_id = Column(ForeignKey("task.id"))
    task = relationship("Task", back_populates="status")

    def __repr__(self):
        return f"Task Status: {self.status}"



def create_database(engine):
    Base.metadata.create_all(engine)
