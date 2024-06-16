import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from db import session
from models import Group, Teacher, Student, Subject, Mark


fake = Faker("uk-Ua")

STUDENTS_COUNT = 50
GROUPS_COUNT = 3
SUBJECTS_COUNT = 5
TEACHERS_COUNT = 5
MARKS_COUNT = 20


def insert_groups():
    for _ in range(GROUPS_COUNT):
        group = Group(name=fake.word())

        session.add(group)

    session.commit()


def insert_teachers():
    for _ in range(TEACHERS_COUNT):
        teacher = Teacher(first_name=fake.first_name(), last_name=fake.last_name())

        session.add(teacher)

    session.commit()


def insert_subjects():
    teachers = session.query(Teacher).all()
    for _ in range(SUBJECTS_COUNT):
        subject = Subject(name=fake.words(nb=2), teacher_id=random.choice(teachers).id)

        session.add(subject)

    session.commit()


def insert_students():
    groups = session.query(Group).all()
    for _ in range(STUDENTS_COUNT):
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            group_id=random.choice(groups).id,
        )

        session.add(student)

    session.commit()


def insert_marks():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    for _ in range(STUDENTS_COUNT):
        for _ in range(MARKS_COUNT):
            mark = Mark(
                mark=random.randint(0, 100),
                mark_date=fake.date_this_year(),
                student_id=random.choice(students).id,
                subject_id=random.choice(subjects).id,
            )

            session.add(mark)

    session.commit()


if __name__ == "__main__":
    try:
        insert_groups()
        insert_teachers()
        insert_subjects()
        insert_students()
        insert_marks()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
        pass
