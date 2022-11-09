# sqlalchemy

## in memory

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlalchemy/in-memory.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlalchemy/in-memory.py -->
```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine_and_session_cls(echo=True):
    engine = create_engine("sqlite:///:memory:", echo=echo)
    session_class = sessionmaker(bind=engine)
    return engine, session_class
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## job_status

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlalchemy/job_status.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlalchemy/job_status.py -->
```py
from enum import Enum
class JobStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    IN_PROGRESS = "IN PROGRESS"
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## schema

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlalchemy/schema.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlalchemy/schema.py -->
```py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from . import JobStatus

Base = declarative_base()


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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## session_scope

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlalchemy/session_scope.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlalchemy/session_scope.py -->
```py
from contextlib import contextmanager


@contextmanager
def session_scope(session_cls):
    session = session_cls()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## sessionmaker_engine_creator

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlalchemy/sessionmaker_engine_creator.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlalchemy/sessionmaker_engine_creator.py -->
```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine_and_session_cls(echo=True):
    # engine = create_engine(f"sqlite:///{db_path}?cache=shared", echo=False, connect_args={'check_same_thread': False})
    # "mysql+pymysql://username:password@localhost/db_name"
    # "mysql://username:password@localhost:3313/xing"
    
    engine = create_engine("sqlite:///:memory:", echo=echo)
    session_class = sessionmaker(bind=engine)
    return engine, session_class


path_to_database = os.environ.get("PATH_TO_SQLITE")
if path_to_database:
    path_to_database = f"sqlite://{path_to_database}?cache=shared"
else:
    path_to_database = f"sqlite:///:memory:?cache=shared"
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## test_create_tables

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlalchemy/test_create_tables.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlalchemy/test_create_tables.py -->
```py
from . import create_database, Job
from . import session_scope
from . import get_engine_and_session_cls


def test_create_in_memory_database():
    engine, session_cls = get_engine_and_session_cls()

    with session_scope(session_cls) as session:
        create_database(engine)
        assert len(session.query(Job).all()) == 0
```
<!-- MARKDOWN-AUTO-DOCS:END -->


