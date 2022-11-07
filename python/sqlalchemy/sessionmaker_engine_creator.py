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


