import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Student, Subject, get_db


TEST_DATABASE_URL = "postgresql://postgres:Vlada@2006@localhost:5432/42704_test"

@pytest.fixture(scope="session")
def engine():
    """Создаем engine для тестовой БД"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    """Создаем сессию для каждого теста"""
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