import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Subject, Grade, get_session
import os

# Конфигурация подключения к БД
# Замените на свои данные
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


@pytest.fixture(scope='function')
def db_session():
    """Фикстура для создания чистой сессии БД для каждого теста"""
    # Создаем движок для тестовой БД
    engine = create_engine(DATABASE_URL)
    
    # Создаем все таблицы
    Base.metadata.create_all(engine)
    
    # Создаем сессию
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Откатываем любые незавершенные транзакции
    session.rollback()
    
    # Удаляем все данные из таблиц после теста
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    
    # Закрываем сессию
    session.close()
    
    # Удаляем таблицы
    Base.metadata.drop_all(engine)


class TestStudentOperations:
    """Тесты для операций со студентами"""
    
    def test_add_student(self, db_session):
        """Тест добавления студента"""
        # Создаем нового студента
        new_student = Student(
            name="Иван Петров",
            email="ivan.petrov@example.com"
        )
        
        # Добавляем в БД
        db_session.add(new_student)
        db_session.commit()
        
        # Проверяем, что студент добавлен
        saved_student = db_session.query(Student).filter_by(
            email="ivan.petrov@example.com"
        ).first()
        
        assert saved_student is not None
        assert saved_student.name == "Иван Петров"
        assert saved_student.email == "ivan.petrov@example.com"
        assert saved_student.id is not None
    
    def test_update_student(self, db_session):
        """Тест изменения данных студента"""
        # Сначала создаем студента
        student = Student(
            name="Анна Сидорова",
            email="anna.sidorova@example.com"
        )
        db_session.add(student)
        db_session.commit()
        
        # Обновляем данные студента
        student.name = "Анна Смирнова"
        student.email = "anna.smirnova@example.com"
        db_session.commit()
        
        # Проверяем, что данные обновились
        updated_student = db_session.query(Student).filter_by(id=student.id).first()
        assert updated_student.name == "Анна Смирнова"
        assert updated_student.email == "anna.smirnova@example.com"
    
    def test_delete_student(self, db_session):
        """Тест удаления студента"""
        # Создаем студента для удаления
        student = Student(
            name="Петр Иванов",
            email="petr.ivanov@example.com"
        )
        db_session.add(student)
        db_session.commit()
        
        student_id = student.id
        
        # Удаляем студента
        db_session.delete(student)
        db_session.commit()
        
        # Проверяем, что студент удален
        deleted_student = db_session.query(Student).filter_by(id=student_id).first()
        assert deleted_student is None


class TestSubjectOperations:
    """Тесты для операций с предметами"""
    
    def test_add_subject(self, db_session):
        """Тест добавления предмета"""
        new_subject = Subject(
            name="Математика",
            credits=5
        )
        
        db_session.add(new_subject)
        db_session.commit()
        
        saved_subject = db_session.query(Subject).filter_by(
            name="Математика"
        ).first()
        
        assert saved_subject is not None
        assert saved_subject.name == "Математика"
        assert saved_subject.credits == 5
        assert saved_subject.id is not None
    
    def test_update_subject(self, db_session):
        """Тест изменения предмета"""
        subject = Subject(
            name="Физика",
            credits=4
        )
        db_session.add(subject)
        db_session.commit()
        
        subject.name = "Общая физика"
        subject.credits = 5
        db_session.commit()
        
        updated_subject = db_session.query(Subject).filter_by(id=subject.id).first()
        assert updated_subject.name == "Общая физика"
        assert updated_subject.credits == 5
    
    def test_delete_subject(self, db_session):
        """Тест удаления предмета"""
        subject = Subject(
            name="Химия",
            credits=3
        )
        db_session.add(subject)
        db_session.commit()
        
        subject_id = subject.id
        
        db_session.delete(subject)
        db_session.commit()
        
        deleted_subject = db_session.query(Subject).filter_by(id=subject_id).first()
        assert deleted_subject is None


class TestGradeOperations:
    """Тесты для операций с оценками"""
    
    def test_add_grade(self, db_session):
        """Тест добавления оценки"""
        # Создаем необходимые зависимости
        student = Student(
            name="Мария Кузнецова",
            email="maria.kuznetsova@example.com"
        )
        subject = Subject(
            name="Программирование",
            credits=4
        )
        db_session.add_all([student, subject])
        db_session.commit()
        
        # Создаем оценку
        grade = Grade(
            student_id=student.id,
            subject_id=subject.id,
            grade=4.5
        )
        db_session.add(grade)
        db_session.commit()
        
        # Проверяем сохранение
        saved_grade = db_session.query(Grade).filter_by(
            student_id=student.id,
            subject_id=subject.id
        ).first()
        
        assert saved_grade is not None
        assert saved_grade.grade == 4.5
    
    def test_update_grade(self, db_session):
        """Тест изменения оценки"""
        # Создаем зависимости и оценку
        student = Student(
            name="Дмитрий Волков",
            email="dmitry.volkov@example.com"
        )
        subject = Subject(
            name="Базы данных",
            credits=5
        )
        grade = Grade(
            student_id=1,  # временный ID, будет обновлен после commit
            subject_id=1,
            grade=3.0
        )
        
        db_session.add_all([student, subject, grade])
        db_session.commit()
        
        # Обновляем оценку
        grade.grade = 4.0
        db_session.commit()
        
        # Проверяем обновление
        updated_grade = db_session.query(Grade).filter_by(id=grade.id).first()
        assert updated_grade.grade == 4.0
    
    def test_delete_grade(self, db_session):
        """Тест удаления оценки"""
        # Создаем зависимости и оценку
        student = Student(
            name="Елена Морозова",
            email="elena.morozova@example.com"
        )
        subject = Subject(
            name="Алгоритмы",
            credits=4
        )
        grade = Grade(
            student_id=1,
            subject_id=1,
            grade=5.0
        )
        
        db_session.add_all([student, subject, grade])
        db_session.commit()
        
        grade_id = grade.id
        
        # Удаляем оценку
        db_session.delete(grade)
        db_session.commit()
        
        # Проверяем удаление
        deleted_grade = db_session.query(Grade).filter_by(id=grade_id).first()
        assert deleted_grade is None