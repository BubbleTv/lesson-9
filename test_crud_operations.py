import pytest
from sqlalchemy.exc import IntegrityError
from database import Student, Subject, get_db

class TestStudentOperations:
    """Тесты для CRUD операций со студентами"""
    
    def test_add_student(self, db_session, sample_student_data):
        """Тест добавления нового студента"""
       
        new_student = Student(**sample_student_data)
        db_session.add(new_student)
        db_session.commit()
        
       
        student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()
        
        assert student is not None
        assert student.name == sample_student_data["name"]
        assert student.age == sample_student_data["age"]
        assert student.email == sample_student_data["email"]
        assert student.group_name == sample_student_data["group_name"]
        
        
        db_session.delete(student)
        db_session.commit()
        
        
        deleted_student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()
        assert deleted_student is None
    
    def test_update_student(self, db_session, sample_student_data):
        """Тест обновления данных студента"""
       
        student = Student(**sample_student_data)
        db_session.add(student)
        db_session.commit()
        
       
        updated_name = "Петр Сидоров"
        updated_age = 21
        updated_group = "CS-102"
        
        student.name = updated_name
        student.age = updated_age
        student.group_name = updated_group
        db_session.commit()
        
        
        updated_student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()
        
        assert updated_student.name == updated_name
        assert updated_student.age == updated_age
        assert updated_student.group_name == updated_group
        assert updated_student.email == sample_student_data["email"]  
        
        db_session.delete(updated_student)
        db_session.commit()
    
    def test_delete_student(self, db_session, sample_student_data):
        """Тест удаления студента"""
       
        student = Student(**sample_student_data)
        db_session.add(student)
        db_session.commit()
        
        
        student_id = student.id
        
       
        db_session.delete(student)
        db_session.commit()
        
      
        deleted_student = db_session.query(Student).filter_by(id=student_id).first()
        assert deleted_student is None
        
       
        not_found_student = db_session.query(Student).filter_by(
            email=sample_student_data["email"]
        ).first()
        assert not_found_student is None
    
    def test_add_student_duplicate_email(self, db_session, sample_student_data):
        """Тест на добавление студента с дублирующимся email (дополнительный)"""
       
        student1 = Student(**sample_student_data)
        db_session.add(student1)
        db_session.commit()
        
        
        duplicate_data = sample_student_data.copy()
        duplicate_data["name"] = "Другой Студент"
        student2 = Student(**duplicate_data)
        db_session.add(student2)
        
       
        with pytest.raises(IntegrityError):
            db_session.commit()
        
       
        db_session.rollback()
        
        
        db_session.delete(student1)
        db_session.commit()

class TestSubjectOperations:
    """Тесты для CRUD операций с предметами"""
    
    def test_add_subject(self, db_session, sample_subject_data):
        """Тест добавления нового предмета"""
       
        new_subject = Subject(**sample_subject_data)
        db_session.add(new_subject)
        db_session.commit()
        
       
        subject = db_session.query(Subject).filter_by(
            name=sample_subject_data["name"]
        ).first()
        
        assert subject is not None
        assert subject.name == sample_subject_data["name"]
        assert subject.credits == sample_subject_data["credits"]
        
       
        db_session.delete(subject)
        db_session.commit()
        
       
        deleted_subject = db_session.query(Subject).filter_by(
            name=sample_subject_data["name"]
        ).first()
        assert deleted_subject is None
    
    def test_update_subject(self, db_session, sample_subject_data):
        """Тест обновления данных предмета"""
        
        subject = Subject(**sample_subject_data)
        db_session.add(subject)
        db_session.commit()
        
        
        updated_name = "Высшая математика"
        updated_credits = 6
        
        subject.name = updated_name
        subject.credits = updated_credits
        db_session.commit()
        
        
        updated_subject = db_session.query(Subject).filter_by(
            name=updated_name
        ).first()
        
        assert updated_subject.credits == updated_credits
        assert updated_subject.name == updated_name
        
        
        db_session.delete(updated_subject)
        db_session.commit()
    
    def test_delete_subject(self, db_session, sample_subject_data):
        """Тест удаления предмета"""
        
        subject = Subject(**sample_subject_data)
        db_session.add(subject)
        db_session.commit()
        
        
        subject_id = subject.id
        
       
        db_session.delete(subject)
        db_session.commit()
        
       
        deleted_subject = db_session.query(Subject).filter_by(id=subject_id).first()
        assert deleted_subject is None
        
        
        not_found_subject = db_session.query(Subject).filter_by(
            name=sample_subject_data["name"]
        ).first()
        assert not_found_subject is None