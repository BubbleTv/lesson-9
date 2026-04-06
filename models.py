from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    """Модель студента"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String, unique=True)
    group_name = Column(String)

    def __repr__(self):
        return (
            f"<Student(id={self.id}, name='{self.name}', "
            f"email='{self.email}')>"
        )


class Subject(Base):
    """Модель предмета"""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    credits = Column(Integer)

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}')>"