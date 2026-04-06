from models import Subject


class TestSubjectCRUD:
    """Тесты CRUD операций для предмета"""

    def test_add_subject(self, db_session, sample_subject_data):
        """Тест добавления нового предмета"""
        # Создаем новый предмет
        new_subject = Subject(**sample_subject_data)
        db_session.add(new_subject)
        db_session.commit()

        # Проверяем, что предмет добавлен
        subject = db_session.query(Subject).filter_by(
            name=sample_subject_data["name"]
        ).first()

        assert subject is not None
        assert subject.name == sample_subject_data["name"]
        assert subject.credits == sample_subject_data["credits"]

        # Очистка: удаляем созданный предмет
        db_session.delete(subject)
        db_session.commit()

        # Проверяем, что предмет удален
        deleted_subject = db_session.query(Subject).filter_by(
            name=sample_subject_data["name"]
        ).first()
        assert deleted_subject is None

    def test_update_subject(self, db_session, sample_subject_data):
        """Тест обновления данных предмета"""
        # Создаем предмет для теста
        subject = Subject(**sample_subject_data)
        db_session.add(subject)
        db_session.commit()

        # Обновляем данные предмета
        updated_name = "Высшая математика"
        updated_credits = 6

        subject.name = updated_name
        subject.credits = updated_credits
        db_session.commit()

        # Проверяем обновление
        updated_subject = db_session.query(Subject).filter_by(
            name=updated_name
        ).first()

        assert updated_subject.credits == updated_credits
        assert updated_subject.name == updated_name

        # Очистка: удаляем предмет
        db_session.delete(updated_subject)
        db_session.commit()

    def test_delete_subject(self, db_session, sample_subject_data):
        """Тест удаления предмета"""
        # Создаем предмет для теста
        subject = Subject(**sample_subject_data)
        db_session.add(subject)
        db_session.commit()

        # Получаем ID созданного предмета
        subject_id = subject.id

        # Удаляем предмет
        db_session.delete(subject)
        db_session.commit()

        # Проверяем, что предмет удален
        deleted_subject = db_session.query(Subject).filter_by(
            id=subject_id
        ).first()
        assert deleted_subject is None

        # Проверяем, что предмета нет в БД по имени
        not_found_subject = db_session.query(Subject).filter_by(
            name=sample_subject_data["name"]
        ).first()
        assert not_found_subject is None