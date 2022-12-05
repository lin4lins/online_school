import string
from random import choice, randrange, sample, randint
import names
from flask_sqlalchemy import SQLAlchemy

from src.models import Group, Student, Course

NUMBER_OF_GROUPS = 10
NUMBER_OF_STUDENTS = 200


def create_group_name() -> str:
    chars = f"{choice(string.ascii_uppercase)}{choice(string.ascii_uppercase)}"
    nums = f"{randrange(10)}{randrange(10)}"
    return f"{chars}-{nums}"


GROUP_NAMES = [create_group_name() for i in range(NUMBER_OF_GROUPS)]
COURSE_NAMES = ['Art', 'Biology', 'Chemistry', 'English', 'Geography', 'History',
                'Information Technology', 'Literature', 'Math', 'Physics']
STUDENT_NAMES = [(names.get_first_name(), names.get_last_name()) for i in range(NUMBER_OF_STUDENTS)]


def create_groups(database: SQLAlchemy):
    for group_name in GROUP_NAMES:
        group_to_create = Group(name=group_name)
        database.session.add(group_to_create)

    database.session.commit()


def create_courses(database: SQLAlchemy):
    for course_name in COURSE_NAMES:
        course_to_create = Course(name=course_name, description=None)
        database.session.add(course_to_create)

    database.session.commit()


def create_students(database: SQLAlchemy):
    courses = Course.query.all()
    for student_name in STUDENT_NAMES:
        student_to_create = Student(group_id=randint(1, 10),
                                    first_name=student_name[0],
                                    last_name=student_name[1])
        student_courses = sample(courses, randrange(1, 4))
        for course in student_courses:
            student_to_create.courses.append(course)
        database.session.add(student_to_create)

    database.session.commit()
