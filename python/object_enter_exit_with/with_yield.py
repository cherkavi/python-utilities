# the same functionality as enter/exit


def create_session():
    session = settings.Session()
    try:
        # place where it will be returned to client code
        yield session
        # after "with" block in client code execution will be continued
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def provide_session(func):
    with create_session() as session:
        session.merge(SomeDataObject())
        
