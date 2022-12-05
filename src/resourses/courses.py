from flask import Response
from flask_restful import Resource

from src import db
from src.repositories import CourseRepository


class CourseResource(Resource):
    def __init__(self):
        super().__init__()
        self.course_repo = CourseRepository(db)

    def post(self, student_id: int, course_id: int):
        """Registers student to the course
           ---
           parameters:
           - name: student_id
             in: path
             required: true
           - name: course_id
             in: path
             required: true
           responses:
             201:
               description: Created
             404:
               description: Not found
             500:
               description: Internal server error
        """
        self.course_repo.add_student(student_id, course_id)
        return Response(status=201)

    def delete(self, student_id: int, course_id: int):
        """Deletes student from the course
           ---
           parameters:
           - name: student_id
             in: path
             required: true
           - name: course_id
             in: path
             required: true
           responses:
             204:
               description: No data
             404:
               description: Not found
             500:
               description: Internal server error
        """
        self.course_repo.delete_student(student_id, course_id)
        return Response(status=204)
