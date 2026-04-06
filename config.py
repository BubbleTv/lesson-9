import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


class Config:
    """Конфигурация подключения к БД"""
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Vlada@2006')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', '42704')
    TEST_DB_NAME = os.getenv('TEST_DB_NAME', '42704_test')

    @classmethod
    def get_database_url(cls, test=False):
        """Получить URL для подключения к БД"""
        db_name = cls.TEST_DB_NAME if test else cls.DB_NAME
        return (
            f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{db_name}"
        )