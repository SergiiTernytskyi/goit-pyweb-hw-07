from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import (
    declarative_base,
    relationship,
)
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    subjects = relationship("Subject", back_populates="teachers")

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship("Student", back_populates="groups")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    group_id = Column(
        "group_id",
        ForeignKey(
            "groups.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    groups = relationship("Group", back_populates="students")
    marks = relationship("Mark", back_populates="students")

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(
        "teacher_id",
        ForeignKey(
            "teachers.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    teachers = relationship("Teacher", back_populates="subjects")
    marks = relationship("Mark", back_populates="subjects")


class Mark(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    mark_date = Column(Date, nullable=False)
    student_id = Column(
        "student_id",
        ForeignKey(
            "students.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    subject_id = Column(
        "subject_id",
        ForeignKey(
            "subjects.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    students = relationship("Student", back_populates="marks")
    subjects = relationship("Subject", back_populates="marks")
