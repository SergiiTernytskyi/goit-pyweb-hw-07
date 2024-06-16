from sqlalchemy import func, desc, select, and_

from models import Mark, Teacher, Student, Group, Subject
from db import session


def select_01():
    """
    SELECT s.id,
        s.first_name,
        s.last_name,
        AVG(m.mark) as average_mark
    FROM students s
    JOIN marks m ON s.id = m.student_id
    GROUP BY s.id
    ORDER BY average_mark ASC
    LIMIT 5;
    """
    result = (
        session.query(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Student)
        .join(Mark)
        .group_by(Student.id)
        .order_by(desc("average_mark"))
        .limit(5)
        .all()
    )
    return result


def select_02():
    """
    SELECT s.id,
        s.first_name,
        s.last_name,
        AVG(m.mark) as average_mark
    FROM marks m
    JOIN students s ON s.id = m.student_id
    WHERE m.subject_id = 1
    GROUP BY s.id
    LIMIT 1;
    """
    result = (
        session.query(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .join(Student)
        .filter(Mark.subject_id == 1)
        .group_by(Student.id)
        .limit(1)
        .all()
    )
    return result


def select_03():
    """
    SELECT g.name as group,
        AVG(m.mark) as average_mark
    FROM marks m
    JOIN students s ON s.id = m.student_id
    JOIN groups g ON s.group_id = g.id
    JOIN subjects as sub ON m.subject_id = sub.id
    WHERE sub.id = 2
    GROUP BY g.name
    ORDER BY g.name;
    """
    result = (
        session.query(
            Group.name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Subject.id == 1)
        .group_by(Group.name)
        .order_by(Group.name)
        .all()
    )
    return result


def select_04():
    """
    SELECT
        AVG(mark) as average_mark
    FROM marks;
    """
    result = (
        session.query(
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .all()
    )
    return result


def select_05():
    """
    SELECT t.first_name,
        t.last_name,
        s.name AS subject_name
    FROM subjects s
    JOIN teachers t ON s.teacher_id = t.id
    WHERE t.id = 2;
    """
    result = (
        session.query(
            Teacher.first_name,
            Teacher.last_name,
            Subject.name.label("subject_name"),
        )
        .select_from(Subject)
        .join(Teacher)
        .filter(Teacher.id == 1)
        .all()
    )
    return result


def select_06():
    """
    SELECT s.first_name,
        s.last_name
    FROM students s
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 2;
    """
    result = (
        session.query(
            Student.first_name,
            Student.last_name,
        )
        .select_from(Student)
        .join(Group)
        .filter(Group.id == 1)
        .all()
    )
    return result


def select_07():
    """
    SELECT s.first_name,
        s.last_name,
        g.name AS group,
        m.mark
    FROM marks m
    JOIN students s ON m.student_id = s.id
    JOIN groups g ON g.id = s.group_id
    JOIN subjects sub ON sub.id = m.subject_id
    WHERE g.id = 2 AND sub.id = 3
    """
    result = (
        session.query(
            Student.first_name, Student.last_name, Group.name.label("group"), Mark.mark
        )
        .select_from(Mark)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(and_(Group.id == 1, Subject.id == 2))
        .all()
    )
    return result


def select_08():
    """
    SELECT AVG(m.mark) as average_mark
    FROM marks m
    JOIN subjects sub ON sub.id = m.subject_id
    JOIN teachers t ON t.id = sub.teacher_id
    WHERE t.id = 2;
    """
    result = (
        session.query(
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.id == 1)
        .all()
    )
    return result


def select_09():
    """
    SELECT
        sub.name as subject_name
    FROM subjects sub
    JOIN marks m ON m.subject_id = sub.id
    JOIN students s ON s.id = m.student_id
    WHERE s.id = 2
    GROUP BY sub.name;
    """
    result = (
        session.query(Subject.name.label("subject_name"))
        .select_from(Subject)
        .join(Mark)
        .join(Student)
        .filter(Student.id == 1)
        .group_by(Subject.name)
        .all()
    )
    return result


def select_10():
    """
    SELECT
        sub.name as subject_name
    FROM subjects sub
    JOIN marks m ON m.subject_id = sub.id
    JOIN students s ON s.id = m.student_id
    JOIN teachers t ON sub.teacher_id = t.id
    WHERE s.id = 2 AND t.id = 1
    GROUP BY sub.name;
    """
    result = (
        session.query(Subject.name.label("subject_name"))
        .select_from(Subject)
        .join(Mark)
        .join(Student)
        .join(Teacher)
        .filter(and_(Student.id == 2, Teacher.id == 1))
        .group_by(Subject.name)
        .all()
    )
    return result


def select_11():
    """
    SELECT
        AVG(mark) AS average_mark
    FROM marks m
    JOIN students s ON s.id = m.student_id
    JOIN subjects sub ON sub.id = m.subject_id
    JOIN teachers t ON sub.teacher_id = t.id
    WHERE s.id = 1 AND t.id = 3
    GROUP BY sub.name
    """
    result = (
        session.query(func.round(func.avg(Mark.mark), 2).label("average_mark"))
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .filter(and_(Student.id == 1, Teacher.id == 3))
        .group_by(Subject.name)
        .all()
    )
    return result


def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (
        select(func.max(Mark.mark_date))
        .join(Student)
        .filter(and_(Mark.subject_id == 2, Student.group_id == 3))
    ).scalar_subquery()

    result = (
        session.query(
            Student.id, Student.first_name, Student.last_name, Mark.mark, Mark.mark_date
        )
        .select_from(Mark)
        .join(Student)
        .filter(
            and_(
                Mark.subject_id == 2,
                Student.group_id == 3,
                Mark.mark_date == subquery,
            )
        )
        .all()
    )

    return result


if __name__ == "__main__":
    # print(select_01())
    # print(select_02())
    # print(select_03())
    # print(select_04())
    # print(select_05())
    # print(select_06())
    # print(select_07())
    # print(select_08())
    # print(select_09())
    # print(select_10())
    # print(select_11())
    print(select_12())
