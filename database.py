from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config


def get_engine(test=False):
    """Создать engine для подключения к БД"""
    database_url = Config.get_database_url(test=test)
    return create_engine(database_url)


def get_session_factory(engine):
    """Создать фабрику сессий"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session(test=False):
    """Получить сессию для работы с БД"""
    engine = get_engine(test=test)
    SessionLocal = get_session_factory(engine)
    return SessionLocal()