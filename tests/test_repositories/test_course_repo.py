import pytest

from src.models import Course, Student
from src.repositories import CourseRepository
from tests.test_data import COURSE_NAMES


@pytest.fixture
def course_repo(_db):
    return CourseRepository(_db)


@pytest.mark.parametrize("id, test_course_name", enumerate(COURSE_NAMES, start=1))
def test_get_by_id(app, course_repo, id, test_course_name):
    with app.app_context():
        assert course_repo.get_by_id(id).name == test_course_name


def test_add_student(app, course_repo):
    with app.app_context():
        course_repo.add_student(1, 1)
        assert isinstance(Course.query.join(Student, Course.students). \
                          filter((Course.students.any(id=1)) & (Course.id == 1)).first(), Course)


def test_delete_student(app, course_repo):
    with app.app_context():
        course_repo.delete_student(1, 1)
        assert Course.query.join(Student, Course.students). \
                   filter((Course.students.any(id=1)) & (Course.id == 1)).first() is None
