from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine_and_session_cls(echo=True):
    # engine = create_engine(f"sqlite:///{db_path}?cache=shared", echo=False, connect_args={'check_same_thread': False})
    engine = create_engine("sqlite:///:memory:", echo=echo)
    session_class = sessionmaker(bind=engine)
    return engine, session_class
