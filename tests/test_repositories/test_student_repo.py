import pytest

from src.models import Student
from src.repositories import StudentRepository, CourseRepository
from tests.test_data import STUDENT_NAMES, NUMBER_OF_STUDENTS_ON_COURSE


@pytest.fixture
def student_repo(_db):
    return StudentRepository(_db)


@pytest.fixture
def course_repo(_db):
    return CourseRepository(_db)


@pytest.mark.parametrize("id, test_student_name", enumerate(STUDENT_NAMES, start=1))
def test_get_by_id(app, student_repo, id, test_student_name):
    with app.app_context():
        assert student_repo.get_by_id(id).first_name == test_student_name[0]


def test_create(app, student_repo):
    with app.app_context():
        student = Student(first_name="Jeffree", last_name="Star", group_id=2)
        student_repo.create(student)
        assert isinstance(Student.query.filter(
            (Student.first_name == "Jeffree") & (Student.last_name == "Star")).first(), Student)


def test_delete(app, student_repo, course_repo):
    with app.app_context():
        course_repo.add_student(11, 1)
        student_repo.delete(11)
        assert Student.query.filter(
            (Student.first_name == "Jeffree") & (Student.last_name == "Star")).first() is None


@pytest.mark.parametrize("course_name, students_in_course_count",
                         NUMBER_OF_STUDENTS_ON_COURSE.items())
def test_get_all_by_course_name(app, student_repo, course_name, students_in_course_count):
    with app.app_context():
        assert len(student_repo.get_all_by_course_name(course_name)) == students_in_course_count
