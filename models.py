from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    credits = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    subject_id = Column(Integer, nullable=False)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_engine(db_url):
    """Создание подключения к базе данных"""
    return create_engine(db_url)


def create_tables(engine):
    """Создание таблиц в базе данных"""
    Base.metadata.create_all(engine)


def get_session(engine):
    """Создание сессии для работы с БД"""
    Session = sessionmaker(bind=engine)
    return Session()