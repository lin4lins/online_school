from flask_sqlalchemy import SQLAlchemy

from src.models import Student, Course, Group


class Repository:
    def __init__(self, db: SQLAlchemy):
        self.db = db


class CourseRepository(Repository):
    def get_by_id(self, course_id: int):
        return Course.query.filter(Course.id == course_id).first()

    def add_student(self, student_id: int, course_id: int):
        course = self.get_by_id(course_id)
        student = Student.query.filter(Student.id == student_id).first()
        course.students.append(student)
        self.db.session.add(course)
        self.db.session.commit()

    def delete_student(self, student_id: int, course_id: id):
        course = self.get_by_id(course_id)
        student = Student.query.filter(Student.id == student_id).first()
        course.students.remove(student)
        self.db.session.add(course)
        self.db.session.commit()


class StudentRepository(Repository):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)
        self.course_repo = CourseRepository(self.db)

    def create(self, student: Student):
        self.db.session.add(student)
        self.db.session.commit()

    def get_by_id(self, student_id: int):
        return Student.query.filter(Student.id == student_id).first()

    @staticmethod
    def get_all_by_course_name(course_name: str) -> list:
        return Student.query.join(Course, Student.courses).\
            filter(Student.courses.any(name=course_name)).all()

    def delete(self, student_id: int):
        Student.query.filter(Student.id == student_id).delete()
        self.db.session.commit()


class GroupRepository(Repository):
    @staticmethod
    def get_by_name(group_name: str):
        return Group.query.filter(Group.name == group_name).first()

    def get_by_student_count(self, student_count: int) -> list:
        groups = Group.query. \
            join(Student, Student.group_id == Group.id). \
            group_by(Group.id). \
            having(self.db.func.count(Group.students) <= student_count). \
            all()
        return groups
