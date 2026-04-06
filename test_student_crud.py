import pytest
from sqlalchemy.exc import IntegrityError

from models import Student


class TestStudentCRUD:
    """Тесты CRUD операций для студента"""

    def test_add_student(self, db_session, sample_student_data):
        """Тест добавления нового студента"""
        # Создаем нового студента
        new_student = Student(**sample_student_data)
        db_session.add(new_student)
        db_session.commit()

        # Проверяем, что студент добавлен
        student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()

        assert student is not None
        assert student.name == sample_student_data["name"]
        assert student.age == sample_student_data["age"]
        assert student.email == sample_student_data["email"]
        assert student.group_name == sample_student_data["group_name"]

        # Очистка: удаляем созданного студента
        db_session.delete(student)
        db_session.commit()

        # Проверяем, что студент удален
        deleted_student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()
        assert deleted_student is None

    def test_update_student(self, db_session, sample_student_data):
        """Тест обновления данных студента"""
        # Создаем студента для теста
        student = Student(**sample_student_data)
        db_session.add(student)
        db_session.commit()

        # Обновляем данные студента
        updated_name = "Петр Сидоров"
        updated_age = 21
        updated_group = "CS-102"

        student.name = updated_name
        student.age = updated_age
        student.group_name = updated_group
        db_session.commit()

        # Проверяем обновление
        updated_student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()

        assert updated_student.name == updated_name
        assert updated_student.age == updated_age
        assert updated_student.group_name == updated_group
        assert updated_student.email == sample_student_data["email"]

        # Очистка: удаляем студента
        db_session.delete(updated_student)
        db_session.commit()

    def test_delete_student(self, db_session, sample_student_data):
        """Тест удаления студента"""
        # Создаем студента для теста
        student = Student(**sample_student_data)
        db_session.add(student)
        db_session.commit()

        # Получаем ID созданного студента
        student_id = student.id

        # Удаляем студента
        db_session.delete(student)
        db_session.commit()

        # Проверяем, что студент удален
        deleted_student = db_session.query(Student).filter_by(
            id=student_id
        ).first()
        assert deleted_student is None

        # Проверяем, что студента нет в БД по email
        not_found_student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()
        assert not_found_student is None

    def test_add_student_duplicate_email(self, db_session, sample_student_data):
        """Тест на добавление студента с дублирующимся email"""
        # Создаем первого студента
        student1 = Student(**sample_student_data)
        db_session.add(student1)
        db_session.commit()

        # Пытаемся создать второго студента с тем же email
        duplicate_data = sample_student_data.copy()
        duplicate_data["name"] = "Другой Студент"
        student2 = Student(**duplicate_data)
        db_session.add(student2)

        # Ожидаем ошибку IntegrityError из-за уникального email
        with pytest.raises(IntegrityError):
            db_session.commit()

        # Откатываем транзакцию
        db_session.rollback()

        # Очистка: удаляем первого студента
        db_session.delete(student1)
        db_session.commit()