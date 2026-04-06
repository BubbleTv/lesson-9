import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from models import Base


@pytest.fixture(scope="session")
def engine():
    """Создает engine для тестовой БД"""
    database_url = Config.get_database_url(test=True)
    engine = create_engine(database_url)

    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

    yield engine

    # Удаляем все таблицы после тестов
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Создает сессию для каждого теста"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def sample_student_data():
    """Пример данных студента для тестов"""
    return {
        "name": "Иван Петров",
        "age": 20,
        "email": "ivan.petrov@example.com",
        "group_name": "CS-101"
    }


@pytest.fixture
def sample_subject_data():
    """Пример данных предмета для тестов"""
    return {
        "name": "Математика",
        "credits": 5
    }