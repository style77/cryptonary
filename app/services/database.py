from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

from app.models.base import Base


def get_database():
    return SQLAlchemy(model_class=Base)


db = get_database()


@contextmanager
def transaction():
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
