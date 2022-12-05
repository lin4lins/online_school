import os

import psycopg2
import pytest
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.resourses import StudentsResource, StudentResource, StudentsSearch, CourseResource, \
    GroupsSearch
from src.models import Group, Course, Student
from src import create_app, db
from tests.test_data import COURSE_NAMES, GROUP_NAMES, STUDENT_DATA

load_dotenv()
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DATABASE = "testing_db"
TEST_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


def init_postgres_db():
    conn = psycopg2.connect(user=USERNAME, password=PASSWORD)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('CREATE DATABASE ' + DATABASE)
    cur.close()
    conn.close()


def drop_postgres_db():
    conn = psycopg2.connect(user=USERNAME, password=PASSWORD)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('DROP DATABASE IF EXISTS ' + DATABASE + ' WITH (FORCE)')
    cur.close()
    conn.close()


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
    for student_name, group, course_names in STUDENT_DATA:
        student_to_create = Student(group_id=group[0],
                                    first_name=student_name[0],
                                    last_name=student_name[1])
        student_courses = [course for course in courses for course_name in course_names
                           if course_name == course.name]
        for course in student_courses:
            student_to_create.courses.append(course)
        database.session.add(student_to_create)

    database.session.commit()


@pytest.fixture(scope='session')
def postgres_db(request):
    init_postgres_db()
    request.addfinalizer(drop_postgres_db)


@pytest.fixture(scope="session")
def app(postgres_db):
    config = {
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "TESTING": True
    }
    app = create_app(config)

    with app.app_context():
        db.create_all()
        create_courses(db)
        create_groups(db)
        create_students(db)

    return app


@pytest.fixture(scope="session")
def _db(app):
    return db


@pytest.fixture(scope="session")
def api(app):
    api = Api(app)
    api.add_resource(StudentsResource, '/students')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(StudentsSearch, '/students/search')
    api.add_resource(CourseResource, '/courses/<int:course_id>/students/<int:student_id>')
    api.add_resource(GroupsSearch, '/groups/search')
    return api


@pytest.fixture()
def client(app):
    return app.test_client()
