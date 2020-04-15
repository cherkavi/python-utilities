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
