from . import create_database, Job
from . import session_scope
from . import get_engine_and_session_cls


def test_create_in_memory_database():
    engine, session_cls = get_engine_and_session_cls()

    with session_scope(session_cls) as session:
        create_database(engine)
        assert len(session.query(Job).all()) == 0
