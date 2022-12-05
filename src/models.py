from src import db
import click
from flask.cli import with_appcontext

association_table = db.Table('association', db.Model.metadata,
                             db.Column('student_id', db.Integer,
                                       db.ForeignKey('student.id', ondelete="CASCADE")),
                             db.Column('course_id', db.Integer,
                                       db.ForeignKey('course.id', ondelete="CASCADE")))


class Group(db.Model):
    __tablename__ = 'group_'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    students = db.relationship("Student", backref="group")


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group_.id"))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    courses = db.relationship("Course", secondary=association_table, back_populates="students",
                              cascade="all,delete")


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128), nullable=True)
    students = db.relationship("Student", secondary=association_table, back_populates="courses",
                               passive_deletes=True)


@click.command("init-db")
@with_appcontext
def init_db_command():
    from src.fill_db import create_courses, create_groups, create_students
    db.create_all()
    create_courses(db)
    create_groups(db)
    create_students(db)

